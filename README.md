Language word game

Boxes:
xButtons are broken: can be clicked, but do not toggle
x Sticky or not sticky 
xBox color 
x Function to return list of string words
x Implement ordered group
- Implement sprite group add fucntion {name: sprite}--why again?
- Word -> Button -> Word Bubble
- Word bubles are lower in box because preexisting Words are already in them 
- Both Word and Wordbubble add to Box.words
- fix wordbubbles static color border: does not update???
- OK button or any true Button()s does not add to box.words, instead box.items

- Open and close boxes 
- Menu boxes

- check update()s in __init__
- Quest prototypes
- 
- effect planning
  - Smooth/ease in animation for word bubbles
  - text padding ideas:
    - surface.copy()
    - blit to another surface, then blit that 2nd surface