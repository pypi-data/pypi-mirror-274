import os
import shutil
import tempfile
import time
import unittest

import svgterm.main
import svgterm.config

SHELL_INPUT = [
    'echo $SHELL && sleep 0.1;\r\n',
    'date && sleep 0.1;\r\n',
    'uname && sleep 0.1;\r\n',
    'w',
    'h',
    'o',
    'a',
    'm',
    'i\r\n',
    'echo -e "\\033[1;31mbright red fg\\033[0m"\r\n',
    'echo -e "\\033[1;41mbright red bg\\033[0m"\r\n',
    'echo -e "\\033[1mbold\\033[0m"\r\n',
    'echo -e "\\033[3mitalics\\033[0m"\r\n',
    'echo -e "\\033[4munderscore\\033[0m"\r\n',
    'echo -e "\\033[9mstrikethrough\\033[0m"\r\n',
    'exit;\r\n'
]


class TestMain(unittest.TestCase):
    test_cases = [
        [],
        ['-c', 'sh'],
        ['--screen-geometry', '82x19'],
        ['-D', '1234'],
        ['--loop-delay', '1234'],
        ['-g', '82x19'],
        ['--template', 'plain'],
        ['-t', 'plain'],
        ['-s'],
        ['--still-frames'],
        ['--screen-geometry', '82x19', '--template', 'plain'],
        ['output_path', '-g', '82x19', '-t', 'plain', '-c', 'date', '-s'],
        ['--screen-geometry', '82x19', '--template', 'plain', '-s', 'output_path'],
        ['-g', '82x19', '-t', 'plain'],
        ['-m', '42', '-M', '100'],
        ['--min-frame-duration', '42ms', '--max-frame-duration', '100'],
        ['record'],
        ['record', '-c', 'ls'],
        ['record', 'output_path'],
        ['record', 'output_path', '--screen-geometry', '82x19'],
        ['record', '--screen-geometry', '82x19'],
        ['render', 'input_filename'],
        ['render', 'input_filename'],
        ['render', 'input_filename', '--template', 'plain'],
        ['render', 'input_filename', 'output_path'],
        ['render', 'input_filename', 'output_path', '--template', 'plain'],
        ['render', 'input_filename', 'output_path', '-t', 'plain', '-m', '42', '-M', '100'],
        ['render', 'input_filename', 'output_path', '-t', 'plain', '-m', '42', '-s', '-M', '100'],
    ]

    def test_parse(self):
        for args in self.test_cases:
            with self.subTest(case=args):
                cmd, parsed_args = svgterm.main.parse(
                    args=args,
                    templates={'plain': b''},
                    default_template='plain',
                    default_geometry='48x95',
                    default_min_dur=2,
                    default_max_dur=None,
                    default_cmd='sh',
                    default_loop_delay=1000
                )

    @staticmethod
    def run_main(args, process_input):
        # Use pipes in lieu of stdin and stdout
        fd_in_read, fd_in_write = os.pipe()
        fd_out_read, fd_out_write = os.pipe()

        pid = os.fork()
        if pid == 0:
            # Child process
            for line in process_input:
                os.write(fd_in_write, line.encode('utf-8'))
                time.sleep(0.060)
            os._exit(0)

        svgterm.main.main(args, fd_in_read, fd_out_write)

        os.waitpid(pid, 0)
        for fd in fd_in_read, fd_in_write, fd_out_read, fd_out_write:
            os.close(fd)

    def test_main(self):
        _, cast_filename = tempfile.mkstemp(prefix='svgterm_', suffix='.cast')
        svg_filename = cast_filename[:-5] + '.svg'

        with self.subTest(case='record (no filename)'):
            args = ['svgterm', 'record']
            TestMain.run_main(args, SHELL_INPUT)

        with self.subTest(case='record (with filename)'):
            args = ['svgterm', 'record', cast_filename]
            TestMain.run_main(args, SHELL_INPUT)

        with self.subTest(case='record (with geometry)'):
            args = ['svgterm', 'record', '--screen-geometry', '82x19']
            TestMain.run_main(args, SHELL_INPUT)

        with self.subTest(case='record (with command)'):
            args = ['svgterm', 'record', '-c', 'date']
            TestMain.run_main(args, [])

        with self.subTest(case='render (no output filename)'):
            args = ['svgterm', 'render', cast_filename]
            TestMain.run_main(args, [])

        with self.subTest(case='render (with output filename)'):
            args = ['svgterm', 'render', cast_filename, svg_filename]
            TestMain.run_main(args, [])

        with self.subTest(case='render (with delay)'):
            args = ['svgterm', 'render', cast_filename, '-D', '1234']
            TestMain.run_main(args, [])

        with self.subTest(case='render (with template)'):
            args = ['svgterm', 'render', cast_filename, '--template', 'window_frame']
            TestMain.run_main(args, [])

        with self.subTest(case='render (still frames)'):
            args = ['svgterm', 'render', cast_filename, '--still-frames']
            TestMain.run_main(args, [])

        with self.subTest(case='render (still frames with output directory)'):
            # Existing directory
            output_path = tempfile.mkdtemp(prefix='svgterm')
            args = ['svgterm', 'render', cast_filename, output_path, '-s']
            TestMain.run_main(args, [])

            # Non existing directory
            shutil.rmtree(output_path)
            args = ['svgterm', 'render', cast_filename, output_path, '-s']
            TestMain.run_main(args, [])

        with self.subTest(case='record and render custom command'):
            args = ['svgterm', '--command', 'ls']
            TestMain.run_main(args, [])

        with self.subTest(case='record and render on the fly (fallback theme)'):
            args = ['svgterm', '--screen-geometry', '82x19']
            TestMain.run_main(args, SHELL_INPUT)

        with self.subTest(case='record and render on the fly (window_frame_js template)'):
            args = ['svgterm', svg_filename, '--template', 'window_frame_js']
            TestMain.run_main(args, SHELL_INPUT)

        for template in svgterm.config.default_templates():
            with self.subTest(case='record and render on the fly ({} template)'.format(template)):
                args = ['svgterm', '-t', template]
                TestMain.run_main(args, SHELL_INPUT)

        cast_v1_data = '\r\n'.join([
            '{',
            '  "version": 1,',
            '  "width": 80,',
            '  "height": 32,',
            '  "duration": 10,',
            '  "command": "/bin/zsh",',
            '  "title": "",',
            '  "env": {},',
            '  "stdout": [',
            '    [0.010303, "\\u001b[1;31mnico \\u001b[0;34m~\\u001b[0m"],',
            '    [1.136094, "❤ ☀ ☆ ☂ ☻ ♞ ☯ ☭ ☢ € →"],',
            '    [0.853603, "\\r\\n"]',
            '  ]',
            '}',
        ])

        with self.subTest(case='render v1 cast file'):
            _, cast_filename_v1 = tempfile.mkstemp(prefix='svgterm_', suffix='.cast')
            with open(cast_filename_v1, 'w') as cast_file:
                cast_file.write(cast_v1_data)

            args = ['svgterm', 'render', cast_filename_v1, svg_filename]
            TestMain.run_main(args, [])

    def test_integral_duration(self):
        test_cases = [
            '100',
            '100ms',
            '100Ms',
        ]
        for case in test_cases:
            with self.subTest(case=case):
                self.assertEqual(
                    svgterm.main.integral_duration_validation(case),
                    100
                )

