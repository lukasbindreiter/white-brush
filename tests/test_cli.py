import pytest

from white_brush.__main__ import main


class TestCLI:
    def test_main(self):
        # Calling the main method without parameters will result in the help text to be printed
        # and then sys.exit will be called by the argparse module. The tests however should continue
        # therefore the resulting SystemExit exception will be caught here
        with pytest.raises(SystemExit) as sys_exit_event:
            main()

        assert sys_exit_event.type == SystemExit
        assert sys_exit_event.value.code == 2
