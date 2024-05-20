# Please Log Shit Please (or `plsp`)

## Notes

```text
`infoinject` is a module allowing you to 'compile' python source code with added debug information.
this means that the interesting parts of the code stay separate from printing and other debug code.
```

```text
=====================
Pieces of the puzzle.
=====================

Logger 			- The piece that does the logging.

Debug_Context 		- Use this along side with the logger to separate different areas of an application.
			- For example, you may have a rendering context and a physics context inside a game engine.

Debug_Mode 		- Use this to specify different levels of debug information.
			- For example, you may have a "info" mode and a "detail" mode.
			- If the "info" mode is active, any messages that are in the "detail" mode will not be printed.
			- This is because the "detail" mode extends from the "info" mode.
			- If the "detail" mode is active, any messages that are in the "info"
			-   and "detail" mode will be printed.

infoinject 		- The piece that injects the debug information into the source code.
			- Uses the Logger to log the debug information.

formatters/ 		- The pieces that format the debug information.
			- For example, you may want to have the time of the debug information to
			-   be formatted in a specific way.
			- You may also want to have the caller of the debug information to be formatted in a specific way.
			- The formatters may be added onto any specified debug context. Then, when the Logger is used
			-   by said context, the formatters will be used to format the debug information.



====================================
How the pieces relate to each other.
====================================

> Nodes A that is down from node B means that A depends on, or is used by, B.

	Logger
	/ \
	+  +--------------------+
	|                       |
	Debug_Context           Debug_Mode
	|
	formatters/
```
