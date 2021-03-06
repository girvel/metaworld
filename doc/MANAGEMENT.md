# The cycle of development

## Milestones

- A cycle starts with **review & design milestone**, during which the issues for main milestone is created

- Next goes the **major** milestone, that is planned before and can not be edited during itself, because it should show progress. It always ends with a **release task**.

- Also there can be a **minor** milestone to contain all the issues that appear during the **major** and should be fixed before its end. 

## Review & design storm

0. Project should be split to discrete **interface layers** on user-developer continuum. F. e. for metaworld these are:

   1. Game UI itself
   2. YAML assets
   3. Game code
   4. ECS Framework
   
   Each of them represent a separate layer of interaction with the product and demands different levels of developing skills. The first layer is closest to a user and the last is closest to a developer.

1. Put all the ideas you have about the next version on the board. Let them sink for some time, then filter & aggregate them to a whole vision.

2. Describe features you want to see in context of different interface layers going from the user's layer to the developer's one.

3. Aggregate features to tasks.

## Issue handling

- Each issue contains detailed description potentially understandable by other developers.

- Development of each issue should be done in a separate branch. Naming should be done in a separate case from the words of issue's title. For example, issue "Extend processing of YAML" could be named as `extend-yaml-processing`.

- Merge commit should be done in this format:

```
<Issue's title> (closes #<issue's number>)

<Issue's description; github's `- []` checkboxes are replaced with markdown's `-` bulletpoints>
```

- No squash when merge
