# Use these elements with your own agent

This whole site is also published as an agent skill: a SKILL.md file with reference files, in the GitHub repository github.com/techczech/app-design-elements. The skill lists the sixteen elements, the three properties and the tests every app carries. The reference files hold the detail for each element, including the Settings design and the rules for letting an agent use an app.

To use it:

1. Download or clone the repository.
2. Put the folder where your agent reads skills. For Claude Code that is `~/.claude/skills/`. For any other agent, point it at SKILL.md.
3. Ask the agent to design, build, review or retrofit an app against it.

For a new app, the skill asks for every element from the first release. For an existing app, it asks for an element to be adopted fully the next time that part of the app is being worked on, with no partial adoption.

At each release, use the release-check table. Walk the sixteen elements and record each one as met, not applicable (with a reason) or failing. A failing element that applies to every app blocks calling the release done.

Because letting an agent use the app is one of the elements, an app built this way can also be operated by your agent, through the same actions the interface uses and a command line for settings.
