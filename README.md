<html>
<body>
<h1>Current status</h1>
<h4 style="color: #FF0000;">All images will need to have their path updated to reflect their new file location on download</h4>
<p>Roadmap below - Updated daily if I remember</p>

<ul>
  
<li><h4>Done!</h4></li>
<ul>
  <li>Lives - enemies cost 1 life when leaked - death at 0 - displayed on screen</li>
  <li>Tower placement guide</li>
  <li>Towers now automatically target the further along enemy</li>
  <li>EnemyHP scaling</li>
  <li>Money per kill + tower cost (gold) + new colour for invalid tower placement if gold is too low</li>
  <li>Added a "hold space tp place towers" instruction on screen (temporary)</li>
  <li>Added wave pattern + spawning loops</li>
  <li>Different Tower types - Basic, Slammer, Trap</li>
  <li>Tower info pannel when placing - cost (currently affordable?), damage, range, fire rate(rps)  - blit on other side of map to cursor</li>
  <li>Upgrade pannel implimented</li>
  <li>Allow user to drag upgrade pannel to either side</li>
  <li>added smart wave calling</li>
</ul>

<li><h4>Next Steps:</h4></li>
<ul>
  <li>Draw range on top of all towers - currently only draws on top of previously placed towers</li>
  <li>Re-order blit sequence to ensure important stuff doesnt get overlapped!</li>
  <li>Make a display for gold, lives, hours spent debugging, waves, etc</li>
  <li>Gamestate screens - menu, play, pause, etc - needs further work</li>
  <li>Tower upgrades (in-game) - in progress</li>
  <li>Buff items - tower amplifiers (maybe only 1 square instead of 2x2?)</li>
</ul>

<li><h4>Later: (unordered)</h4></li>
<ul>
  <li>Music / SFX?</li>
  <li>Make better art</li>
  <li>Ballence the upgrades, cost, enemy HP and cash flow scaling
  <li>Tower upgrades (perminent "research" style to carry across multiple games)</li>
  <li>Different enemies -pulse to disable towers for a time?</li>
  <li>More different tower types  (Piercing shot, !necrotower!-(enemies that die in its range resurect as allies, 0 dmg), Missile launcher-(min. range?), shotgun tower, ice launcher-(slow effect), flame thrower-(cancels freeze))
buff items - tower amplifiers (maybe only 1 square instead of 2x2?)</li>
  <li>Fuse tower types when in a 2x2 array? (steal from BTTD series)</li>
  <li>Abilities to freeze enemies, buff towers in a zone, place blockades on tracks...</li>
  <li>(maybe not needed) - Launch config window before game (sepperate while loop) to allow user to choose a window size, then impliment a scale function for all rect objects</li>
  <li>Add smart wave calling (if len(enemies)==0, if wave_spawn counter==wavestyle[1], or instantly (currently the only one used))</li>
</ul>
</ul>
<h3>Instructions:</h3>
<p>(big green button is start)
Hold space and press w to select a standard tower, press a to select a Slammer tower, click to place. drag the info box when selecting a tower to move it to the other side (click a tower to select its information, or press esc to close). Towers automatically shoot, you can see your lives in the top left corner, Gold in the top right and wave information is displayed in the terminal. Waves scale up in difficulty and take a random pattern. Right click in the top right to change wave calling modes: RED = instant, YELLOW = when clear, WHITE = on demand (left click to call)</p>
</body>
</html>

