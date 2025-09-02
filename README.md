# Project

A walkthrough this tutorial on writing your own AI coding agent.

## Purpose

To achieve a better understanding of agentic coding agents so that it becomes easier to point out flaws in projects like charm.


## Impressions

- pydantic-ai is a great library for building agentic coding agents with a CLI interface
- Should watch it to see if it adds ACP support for integration with things like the zed editor.

## Reference

- https://martinfowler.com/articles/build-own-coding-agent.html

## My Planned Implementation

Start with an anthropic model using pydantic-ai to eventually integrate a local model.

## Note on models

- Google Gemini models work reasonably well in pydantic-ai
- Anthropic models work well in pydantic-ai
- granite3.3:2b Ollama model works OK in pydantic-ai. It often fails to execute the unit tests. Other ollama models did not work at all at this point in time.

## TODO

- Makes this a portable utility that can be executed across different projects. 
- Make it good at file organization using a local model like granite3.3:2b
