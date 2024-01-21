# from maturin import import_hook

# # install the import hook with default settings
# import_hook.install()
# # or you can specify bindings
# import_hook.install(bindings="pyo3")
# # and build in release mode instead of the default debug mode
# import_hook.install(release=True)
from boards import *

from CrossNumber import RustedBoard

# print(RustedBoard)

# a = RustedBoard(8, 8)
# a.set_value(0, 0, True, 24)

# print(a.is_possible(0, 0, True, 240))
board_yuichiro.solve()
# board_ryder.solve()
