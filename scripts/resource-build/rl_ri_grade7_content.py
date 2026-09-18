"""Original Grade 7 NC ELA reading-standard packets (RL.7.1-3,4,5,6,7,9 and RI.7.1-8).

Replaces the 16 listings a prior automated pass advertised but never produced
files for. Every passage, question, and answer below is original content
written for this batch; no released-test or third-party material is used.
Each item's answer includes its own reasoning, matching the site's existing
daily-literacy answer-key format.
"""
NC='https://www.dpi.nc.gov/documents/publications/catalog/'
ROWS=[]
def add(slug,title,code,standard_text,objective,lesson,models,texts,items,price):
 assert len(items)==20,(slug,len(items))
 assert len(models)==2
 assert len(texts) in (1,2),(slug,len(texts))
 ROWS.append(dict(id='nc-g7-'+slug,title=title,state='North Carolina',grade='7',subject='Reading',
  standard=code+' — '+standard_text,objective=objective,source=NC,resourceType='Complete ELA practice packet',
  lesson=lesson,models=models,texts=texts,
  items=[{'q':q,'answer':a,'work':a} for q,a in items],price=price))

# ---------------------------------------------------------------- RL.7.1
add('rl71-textual-evidence','Textual Evidence Detectives','RL.7.1',
 'Cite several pieces of textual evidence to support analysis of what the text says explicitly as well as inferences drawn from the text.',
 'Cite several pieces of textual evidence to support analysis of explicit statements and inferences drawn from a literary text.',
 'Explicit evidence is stated directly in the text. An inference is a reasonable conclusion built from evidence plus what you already know, not a guess. Strong analysis usually needs more than one piece of evidence. Quote the text or closely paraphrase it, and name the paragraph.',
 [('Paragraph 2 says Mr. Alvarez "checked the mailbox three times before noon." What can you infer, and what is your evidence?',
   'You can infer he is anxious about the letter. Evidence: checking three times before noon shows repeated, unusual attention to something he is waiting for.'),
  ('Is "the garden had tomatoes" an inference or explicit evidence if paragraph 1 states it directly?',
   'Explicit evidence — the text states it directly, so no inference is required.')],
 [('The Last Season', (
   '1. Mr. Alvarez had taught seventh grade for thirty-one years, and for the last twelve of them he had kept a community garden behind the school with his students. Tomatoes climbed a lattice of old broom handles. Bees moved between rows of marigolds planted to keep pests away.\n\n'
   '2. On the first Tuesday in October, he checked the mailbox three times before noon. Each time he walked back to his classroom a little slower than before.\n\n'
   '3. "The district sent a letter about the garden lot," he told his fourth-period class, setting an unopened envelope on his desk. He did not open it. He asked a student to water the tomatoes instead, then stood at the window for the rest of the period.\n\n'
   '4. At lunch, two students, Priya and Deshawn, found him kneeling by the marigolds, pulling weeds that were not really there. "You already did that row," Priya said. He looked at his hands, dirt-streaked, and laughed quietly. "Habit," he said.\n\n'
   '5. That afternoon he finally opened the letter in front of the class. He read it twice, silently, before speaking. "They are selling the lot next spring. A parking structure." His voice stayed level, but he set the letter down instead of folding it.\n\n'
   '6. Deshawn asked if the garden could move. Mr. Alvarez said maybe, if a new plot could be found before spring, but plots that size were hard to come by near the school. He did not promise anything.\n\n'
   '7. For the rest of the week, he brought his classes outside every day instead of the usual twice. He photographed the tomatoes, the bent broom handles, the bees. On Friday he pinned the photographs to the class bulletin board under a hand-lettered sign: "Twelve seasons. Keep looking."'))],
 [('What does paragraph 2 state explicitly about Mr. Alvarez\'s morning?','He checked the mailbox three times before noon.'),
  ('What can you infer about why he checked the mailbox repeatedly? Cite evidence.','He was anxious about a letter he was expecting; checking three times before noon (paragraph 2) shows unusual, repeated attention to the mail.'),
  ('What explicit action shows he avoided the letter in paragraph 3?','He set it on his desk unopened and had a student water the tomatoes instead of doing it himself.'),
  ('What can you infer from him standing at the window for the rest of the period? Cite evidence.','He was distracted or worried; paragraph 3 states he stood at the window instead of teaching or working, right after avoiding the letter.'),
  ('What explicit detail shows Priya noticed something odd about his weeding?','She said, "You already did that row."'),
  ('What can you infer about Mr. Alvarez\'s state of mind from the weeding detail in paragraph 4? Cite two pieces of evidence.','He was distracted and not fully present; evidence includes pulling weeds that were not there and repeating a row Priya says he already did.'),
  ('What does the text state explicitly about how he read the letter in paragraph 5?','He read it twice, silently, before speaking.'),
  ('What can you infer from him setting the letter down instead of folding it? Cite evidence.','He was troubled by the news; paragraph 5 notes his voice "stayed level, but he set the letter down instead of folding it," suggesting composure that does not match his actions.'),
  ('What explicit fact does the letter contain?','The district is selling the garden lot next spring to build a parking structure.'),
  ('What can you infer about how certain a new garden plot is? Cite evidence.','It is uncertain; paragraph 6 states he said "maybe" and that he "did not promise anything," and that plots that size were hard to come by.'),
  ('What explicit change does Mr. Alvarez make in paragraph 7?','He brings his classes outside every day instead of the usual twice.'),
  ('What can you infer about why he photographs the garden that week? Cite evidence.','He wants to preserve a record of the garden before it may be gone; this follows immediately after learning the lot will be sold, and he photographs specific, familiar features like the tomatoes and broom handles.'),
  ('What does the bulletin board sign state explicitly?','"Twelve seasons. Keep looking."'),
  ('What can you infer the sign means, using evidence from the story?','It likely means the garden\'s value continues even if its future is uncertain, and students should keep noticing what is around them; this follows the deliberate act of photographing and displaying twelve years of the garden.'),
  ('Cite two pieces of evidence that Mr. Alvarez cares deeply about the garden.','He has kept it for twelve years (paragraph 1), and he photographs it and makes a bulletin board display after learning it may close (paragraph 7).'),
  ('Cite evidence that the students notice his mood shift, and explain the inference it supports.','Priya comments on his repeated weeding (paragraph 4); this supports the inference that his distress is visible enough for students to notice.'),
  ('Why might the author choose not to have Mr. Alvarez cry or raise his voice? Use evidence to support your inference.','It suggests he manages difficult feelings quietly; the text explicitly says his "voice stayed level" even while his actions (setting down the letter, pulling nonexistent weeds) reveal distress.'),
  ('Is it explicit or an inference that the garden will definitely close? Explain using the text.','It is not fully certain — the letter states the lot will be sold, which is explicit, but paragraph 6 explicitly says finding a new plot is only a "maybe," so the story leaves the final outcome open.'),
  ('Combine two pieces of evidence to support the inference that Mr. Alvarez is trying to give students a lasting memory of the garden.','He brings classes outside daily instead of twice (paragraph 7) and photographs the garden\'s features, then displays them with a sign about continuing to look — together these actions suggest he wants the garden remembered even if it closes.'),
  ('Write one full inference about Mr. Alvarez, with two pieces of cited evidence supporting it.','Answers vary; require a stated inference plus two specific, correctly cited details from the passage that reasonably support it, not just restated events.')],
 500)

# ---------------------------------------------------------------- RL.7.2
add('rl72-theme-summary','Theme Trackers','RL.7.2',
 'Determine a theme of a text and analyze its development over the course of the text; provide an objective summary of the text.',
 'Determine a theme of a literary text, analyze how it develops across the text, and write an objective summary.',
 'A theme is a message about life the story teaches, not just its topic. An objective summary reports only what happens, in order, without your opinions or added details. Track how a character\'s actions or thinking change from the beginning to the end to find how the theme develops.',
 [('Topic: friendship. Possible theme?','A true friend supports you even when it is inconvenient — a complete sentence describing a lesson, not just a one-word topic.'),
  ('Is "the team lost the first three games" an objective summary sentence or an opinion?','Objective — it reports a plot fact without judgment. "The team foolishly lost" would add opinion.')],
 [('Second String', (
   '1. Renata had played second-string goalkeeper for two seasons. She knew the starting keeper\'s habits better than her own: how Coach Yu warmed up, which drills the team ran on rainy days, how long the equipment closet stuck before it opened.\n\n'
   '2. In the third game of the season, the starting keeper, Bea, rolled her ankle in warm-ups. Coach Yu looked down the bench. "Renata, you\'re in."\n\n'
   '3. Renata\'s first save came in the ninth minute, a low shot she barely reached. Her second came in the twentieth, a header she caught cleanly. By halftime her hands were raw from the gloves, but the score was still 0–0.\n\n'
   '4. In the second half, an opposing forward broke free. Renata came off her line too early, and the ball slipped past her into the net. She heard someone on the bench groan. She did not look at them.\n\n'
   '5. "Reset," Coach Yu called from the sideline. Renata nodded, more to herself than to him, and moved back into position for the next play.\n\n'
   '6. With four minutes left, the same forward broke free again. This time Renata held her line, waited, and smothered the shot at the forward\'s feet. The whistle blew. Her team had lost 1–0, but she had made six saves in her first start.\n\n'
   '7. After the game, Bea, on crutches, met her at the equipment closet. "You held your line that last time," Bea said. "That\'s the part I still mess up." Renata realized she had spent two seasons learning the game by watching someone she had assumed was simply better than her.\n\n'
   '8. The next week, Coach Yu posted the lineup. Renata\'s name was listed first.'))],
 [('What is the topic of this story in one or two words?','Soccer, or goalkeeping — the general subject, not yet a full theme statement.'),
  ('State a possible theme of the story as a full sentence.','Preparation lets you rise to an opportunity even when it comes unexpectedly — or an equivalent full-sentence life lesson supported by the story.'),
  ('What explicit event starts Renata\'s chance to play?','Bea rolls her ankle in warm-ups before the third game.'),
  ('How does Renata react to her first mistake in paragraph 4? Cite the text.','She does not look at the bench when someone groans; she does not react outwardly to the error.'),
  ('What does Coach Yu say after her mistake, and what does it suggest about the theme?','He says "Reset," suggesting the theme includes recovering focus after a setback rather than dwelling on it.'),
  ('How does Renata\'s action in paragraph 6 show change or growth from paragraph 4?','In paragraph 4 she comes off her line too early and is scored on; in paragraph 6 she holds her line and stops the same kind of attack, showing she adjusted her approach.'),
  ('What does Bea\'s comment in paragraph 7 reveal about Renata\'s past view of herself?','Renata had assumed Bea was simply better than her, but Bea says holding the line is something she herself still struggles with, showing Renata underestimated her own growth.'),
  ('How does the story\'s ending develop the theme? Cite evidence.','Coach Yu lists Renata\'s name first on the new lineup, showing that her preparation and improvement during the game earned a lasting opportunity, not just a one-game fill-in.'),
  ('Which theme fits the story better: "Winning is the only measure of success" or "Growth can come from failure that leads to recovery"? Explain with evidence.','"Growth can come from failure that leads to recovery" fits better; the team loses 1–0, yet Renata\'s recovery after her mistake and Bea\'s comment show personal growth mattered more than the score.'),
  ('Write one objective sentence summarizing paragraphs 1–2 (no opinions).','Renata had played second-string goalkeeper for two seasons, and when the starting keeper was injured in the third game, the coach put her in.'),
  ('Write one objective sentence summarizing paragraph 4 (no opinions).','An opposing forward broke free, Renata left her line early, and the ball went into the net.'),
  ('Identify one word in this draft summary that is an opinion, not a fact: "Renata bravely and skillfully made her first save."','Bravely (or skillfully) — these describe the writer\'s judgment of the save, not an observable fact from the text.'),
  ('Write an objective one-sentence summary of the story\'s ending.','Renata made six saves in her first start, her team lost 1–0, and the coach listed her name first on the next lineup.'),
  ('Why is "Renata was clearly the best player on the team" not appropriate for an objective summary?','It is an opinion and an overstatement not directly supported by the text, which only shows her performance in one game.'),
  ('Combine paragraphs 3, 4, and 6 into one two-sentence objective summary.','Renata made two saves in the first half to keep the score at 0–0. In the second half she was scored on once after leaving her line early, but she recovered to stop the same forward late in the game.'),
  ('How does Bea\'s appearance on crutches at the end connect to the theme? Cite evidence.','It shows the story values Bea\'s honest acknowledgment of Renata\'s growth ("That\'s the part I still mess up"), reinforcing that skill and confidence develop over time for both characters.'),
  ('Trace one specific way the theme develops from the middle to the end of the story.','In the middle, Renata\'s mistake in paragraph 4 shows a gap in her readiness; by paragraph 6 she applies what she learned to succeed in the same situation, showing the theme of growth developing through direct experience.'),
  ('Is "the team lost 1–0" objective or subjective? Explain.','Objective — it is a verifiable fact stated in the text, without added judgment.'),
  ('Write a two-sentence objective summary of the whole story.','After the starting goalkeeper was injured, a second-string player got her first start and made several saves despite one early mistake. Her team lost by one goal, but her performance earned her the top spot on the next lineup.'),
  ('State the theme in one sentence and support it with one piece of cited evidence.','Answers vary; require a complete theme statement (a lesson, not just a topic) plus one specific, correctly cited detail from the story that supports it.')],
 550)

# ---------------------------------------------------------------- RL.7.3
add('rl73-story-elements','Story Element Interactions','RL.7.3',
 'Analyze how particular elements of a story or drama interact (e.g., how setting shapes the characters or plot).',
 'Analyze how setting, character, and plot interact in a literary text, explaining how changes in one element affect the others.',
 'Setting is when and where a story happens. Character is who is in it and how they think, feel, and act. Plot is what happens and why. These elements interact when a change in one causes a change in another — for example, when weather (setting) forces a character to make a new choice (plot).',
 [('If a blizzard (setting) strands two characters in a cabin, how might that affect plot?','It could force them to talk or cooperate out of necessity, creating plot events that would not happen otherwise — the setting change drives new character interaction.'),
  ('If a character is naturally stubborn, how might that shape how they respond to a setting change like moving to a new town?','A stubborn character might resist adapting to the new setting longer than another character would, which could slow or complicate the plot\'s resolution.')],
 [('New Ground', (
   '1. Nadia had lived in an apartment her whole life, three floors up from a street that never quite went quiet. When her mother took a job managing a horse farm two hours outside Raleigh, Nadia packed one box of things she cared about and left the rest.\n\n'
   '2. The farm had forty acres, a barn that leaned slightly to the left, and an aging horse named Copper who belonged to the farm\'s owner. Nadia had never been near a horse larger than a photograph.\n\n'
   '3. For the first two weeks, she stayed inside after school, reading in the room that used to be a hayloft. Her mother asked her to help feed the horses. Nadia found reasons not to.\n\n'
   '4. One afternoon, a thunderstorm knocked out the farm\'s power. Nadia\'s mother was in town buying a generator part, and the owner had gone with her. Nadia, alone, heard Copper kicking the inside of his stall.\n\n'
   '5. She had read enough, in her apartment years, to know that horses could hurt themselves in a panic. She also knew no one was coming for at least an hour. She walked to the barn in the rain, telling herself she was only checking the latch.\n\n'
   '6. Copper\'s stall door had come loose in the wind, banging against the frame with each gust, which was what had spooked him. Nadia, hands shaking, wedged a feed bucket against the door to hold it still, then stood outside the stall, talking in the low, steady voice she used for nothing in particular, until his kicking slowed and stopped.\n\n'
   '7. When her mother returned, she found Nadia sitting on an overturned bucket outside Copper\'s stall, soaked, with the horse\'s nose resting against her shoulder through the bars. "I thought you didn\'t want anything to do with the horses," her mother said. "I didn\'t," Nadia said. "But nobody else was here."\n\n'
   '8. She still missed the apartment sometimes. But she started going to the barn every afternoon after that, not because her mother asked, and not because she had stopped missing the city, but because Copper, it turned out, did not care whether she liked the farm yet.'))],
 [('What explicit setting change happens in paragraph 1?','Nadia moves from a city apartment to a horse farm two hours outside Raleigh.'),
  ('How does Nadia\'s character (her comfort with the city, her reluctance) shape her early behavior at the farm? Cite evidence.','She stays inside reading and avoids helping with the horses, showing her discomfort with the new setting shapes her choice to withdraw rather than engage.'),
  ('What plot event in paragraph 4 forces a change in setting conditions?','A thunderstorm knocks out the power while Nadia is alone at the farm.'),
  ('How does that setting change (the storm, being alone) interact with plot — what does it force Nadia to do?','It forces her to decide whether to help Copper herself, since no other adult is available, pushing the plot forward through her choice to act.'),
  ('How does Nadia\'s established character (cautious, avoids the barn) make her walk to the barn in paragraph 5 significant?','It shows a real change in her behavior — someone who had been avoiding the horses is now choosing to face her fear because of the setting\'s emergency conditions.'),
  ('What causes Copper\'s panic, according to paragraph 6?','His stall door had come loose in the wind and was banging against the frame with each gust.'),
  ('How does Nadia\'s solution in paragraph 6 show interaction between setting (the storm, the loose door) and character (her calm response)?','The storm creates the physical problem (the banging door), and Nadia\'s character — steady, resourceful under pressure — allows her to solve it by wedging the bucket and using a calm voice.'),
  ('How does the setting of the barn (an enclosed, quiet space) support the plot moment where Copper calms down?','The barn\'s enclosed space lets Nadia\'s steady voice reach Copper consistently, without outside distraction, supporting the plot resolution of his panic.'),
  ('What does Nadia\'s explanation to her mother in paragraph 7 ("nobody else was here") reveal about how the plot changed her character?','It shows she acted out of necessity rather than a change of heart about the farm, revealing that circumstance, not preference, drove her actions — an honest, understated character response.'),
  ('How does the ending in paragraph 8 show a new interaction between character and setting?','Nadia starts choosing to go to the barn daily, showing the setting (the farm, Copper) has begun to shape her character\'s habits and attachments, even though she still misses the city.'),
  ('Would the plot event in paragraphs 4–6 have happened the same way if the story stayed in the city apartment? Explain.','No; the plot depends on the farm setting (a horse, a barn, a storm-prone rural location) — an apartment would not create the same conditions for this specific conflict and resolution.'),
  ('How does Copper, as a character element, affect Nadia\'s plot arc?','Copper does not react to Nadia\'s feelings about the move, which paragraph 8 suggests helps her connect to the farm on the horse\'s terms rather than needing to resolve her feelings about the city first.'),
  ('Identify one setting detail from paragraph 2 and explain how it might later matter to plot.','The barn "leaned slightly to the left" or Copper "belonged to the farm\'s owner" — either detail establishes the farm\'s slightly worn, real conditions that make the storm-related stall trouble in paragraph 6 more plausible.'),
  ('How do Nadia\'s two settings (apartment vs. farm) interact with her sense of identity by the story\'s end?','She still misses the apartment, but the farm setting has begun shaping a new part of her identity through her connection to Copper, showing both settings coexist in her character rather than one simply replacing the other.'),
  ('Explain how the timing of the storm (paragraph 4) affects which character has to act.','Because her mother and the farm owner are both away, the storm\'s timing isolates Nadia specifically, making her the only one available to respond — this setting detail directly shapes which character drives the plot.'),
  ('How might the story be different if Nadia\'s mother had been present during the storm?','Nadia\'s mother likely would have handled Copper, removing the moment that forces Nadia\'s character growth — the setting detail of her being alone is essential to the plot\'s effect on her character.'),
  ('Cite evidence that Nadia\'s actions during the storm are shaped by what she already knew, not just instinct.','Paragraph 5 states she "had read enough, in her apartment years, to know that horses could hurt themselves in a panic," showing her city-setting knowledge unexpectedly helps her in the new farm setting.'),
  ('How does the interaction between setting and plot in this story support the idea that new environments can reveal character traits a person did not know they had?','The unfamiliar farm setting creates a crisis (the storm) that reveals Nadia\'s calm, capable side, a trait not shown earlier in the story when she was avoiding the barn — the new setting is what makes the trait visible through plot events.'),
  ('Explain one way plot events in this story could not have unfolded without a specific setting detail.','The stall door banging in the wind (a setting detail) directly causes Copper\'s panic (a plot event); without that specific setting detail, the central conflict would not occur.'),
  ('Choose one interaction (setting–character, setting–plot, or character–plot) and explain it fully with two pieces of textual evidence.','Answers vary; require a clearly named interaction type and two specific, correctly cited details showing how one element affects the other.')],
 500)

# ---------------------------------------------------------------- RL.7.4
add('rl74-word-meaning-sound','Word Meaning and Sound Devices','RL.7.4',
 'Determine the meaning of words and phrases as they are used in a text; analyze the impact of rhymes and repetitions of sounds on meaning and tone.',
 'Determine word meaning using context clues in prose and analyze how rhyme and repetition of sounds affect meaning and tone in a poem.',
 'Context clues are nearby words or sentences that hint at an unfamiliar word\'s meaning. In poetry, rhyme and repeated sounds (alliteration, assonance) are not just decoration — they can slow a reader down, create a mood, or emphasize an idea. Read a poem aloud, even silently, to notice its sound.',
 [('"The tide receded, leaving the sand pocked with shallow pools." What does "receded" likely mean, and what clue helped?','Moved back or retreated — the clue is "leaving the sand" exposed, which only makes sense if the water pulled away.'),
  ('In "the wind whipped and whistled," what sound device is used, and what mood does it create?','Alliteration (repeated w sound) and it creates a harsh, restless, unsettled mood matching the wind\'s force.')],
 [('After the Storm (prose excerpt)', (
   'The harbor the morning after looked like it had aged ten years overnight. Boats that had strained at their moorings now sat crookedly, their hulls scraped raw where they had knocked against the dock. Gulls picked through debris with a kind of businesslike indifference, as if this happened every week.\n\n'
   'Old Mr. Petrides stood at the end of the pier, surveying the wreckage of his bait shop\'s awning, torn clean from its posts. He did not look angry. He looked, instead, resigned, the way a person looks at a bill they already knew was coming.\n\n'
   '"Could\'ve been worse," he said to no one, and began, methodically, to coil a length of rope that had washed loose in the night.')),
  ('Harbor, After', (
   'The wind whipped and whistled, wild and wide,\n'
   'It battered the boats where they bobbed and cried.\n'
   'The gulls, unbothered, glided and grinned,\n'
   'While ropes lay tangled, twisted, and thinned.\n\n'
   'The old man stood where the pier met the sea,\n'
   'Still as the water was choosing to be.\n'
   'He counted his losses in murmurs, not moans,\n'
   'A harbor rebuilding itself, stone by stone.'))],
 [('What does "moorings" most likely mean, based on the first paragraph\'s context?','The ropes, chains, or fixed points that hold a boat in place — the boats "strained at their moorings," suggesting something restraining them.'),
  ('What context clue helps define "moorings"?','"Boats that had strained at their moorings now sat crookedly" — the strain implies something was holding them, and the crooked result after the storm confirms it.'),
  ('What does "indifference" mean as used to describe the gulls?','A lack of concern or interest — the gulls are described as picking through debris in a "businesslike" way, suggesting they are unaffected emotionally.'),
  ('What context clue supports that meaning of "indifference"?','The phrase "as if this happened every week" suggests the gulls are unbothered by the destruction, matching a definition of not caring.'),
  ('What does "resigned" mean as it describes Mr. Petrides?','Accepting something unwanted without resistance — the text compares his look to someone facing "a bill they already knew was coming," which is a resigned, expected acceptance.'),
  ('Why does the author compare Mr. Petrides\'s expression to someone looking at an expected bill?','It shows he is not surprised or overwhelmed by the storm\'s damage, just quietly accepting it as something he anticipated.'),
  ('Identify one example of alliteration in the poem\'s first stanza.','"whipped and whistled, wild and wide" or "bobbed and cried" — repeated initial sounds across nearby words.'),
  ('How does the alliteration in "whipped and whistled, wild and wide" affect the poem\'s tone?','It creates a harsh, forceful sound that mimics the storm\'s intensity, reinforcing a tone of chaos or violence.'),
  ('Find one rhyme pair in the second stanza and explain what feeling it helps create.','"sea/be" or "moans/stones" — the steady rhyme creates a calmer, more controlled feeling that contrasts with the storm\'s chaos, matching the old man\'s quiet acceptance.'),
  ('How does the poem\'s tone shift between the first and second stanzas?','The first stanza\'s harsh sounds create a chaotic, violent tone describing the storm; the second stanza\'s steadier, quieter sounds shift the tone to calm acceptance, focused on the old man.'),
  ('What does "unbothered" mean in "The gulls, unbothered, glided and grinned"? Use context.','Not troubled or affected — this matches the prose description of the gulls\' "businesslike indifference," showing both texts describe the same lack of concern.'),
  ('Why might the poet choose the word "grinned" to describe the gulls, even though gulls cannot literally grin?','It personifies the gulls, suggesting an almost mocking or careless attitude toward the destruction, similar to the "indifference" described in the prose.'),
  ('What does "rebuilding itself, stone by stone" suggest about the harbor\'s recovery?','That recovery will be slow and steady, happening in small, deliberate steps rather than all at once.'),
  ('How does the repeated -st sound in "still," "stone by stone" affect the poem\'s ending?','It creates a slow, steady rhythm that reinforces the idea of gradual, patient rebuilding, matching the calm tone of the final lines.'),
  ('Compare the mood created by sound devices in stanza 1 to the mood of the prose excerpt\'s first paragraph.','Both are chaotic and unsettled — the prose describes crooked, scraped boats and indifferent gulls, while the poem\'s harsh alliteration ("whipped and whistled") creates a similarly turbulent mood.'),
  ('What word in the poem means the same as "resigned" from the prose excerpt, based on context?','"Still" — "Still as the water was choosing to be" suggests calm acceptance, matching the prose\'s description of Mr. Petrides as resigned.'),
  ('Explain how repetition of the "o" sound in "moans... stone by stone" contributes to tone.','The repeated long "o" sound slows the reading pace, creating a mournful but steady tone that matches quiet acceptance rather than despair.'),
  ('Why is "counted his losses in murmurs, not moans" an effective description of the old man\'s reaction?','It shows restraint — murmurs are quiet and controlled, while moans would suggest louder distress, matching his resigned, undramatic response in the prose.'),
  ('Using both texts, explain how word choice and sound work together to build the same overall impression of the old man.','Both texts show him as calm and accepting rather than devastated; the prose\'s "resigned" description and the poem\'s steady rhymes and soft sounds ("still," "stone by stone") reinforce this same controlled, quiet response to loss.'),
  ('Choose one word from either text whose precise meaning changes how you understand a sentence, and explain using context.','Answers vary; require a specific word, a context clue used to define it, and an explanation of how that meaning shapes understanding of the sentence or passage.')],
 550)

# ---------------------------------------------------------------- RL.7.5
add('rl75-form-structure','Form, Structure, and Meaning','RL.7.5',
 'Analyze how a drama\'s or poem\'s (or other literary genre\'s) form or structure contributes to its meaning.',
 'Analyze how the form and structure of a sonnet and a free verse poem each contribute to meaning, and compare how the same theme is shaped differently by each form.',
 'A sonnet has a fixed structure: 14 lines, a specific rhyme scheme, and often a "turn" where the idea shifts. Free verse has no fixed rhyme or line pattern, letting its structure mirror its content more freely. The same theme can feel very different depending on which form delivers it.',
 [('A poem with a strict rhyme scheme discusses a chaotic storm. What effect might that contrast create?','It could create tension between the poem\'s orderly form and its chaotic subject, or suggest the speaker is trying to impose control on something uncontrollable.'),
  ('A free verse poem about a racing heartbeat uses short, irregular lines. Why might that structure fit the content?','Short, irregular lines can mimic the unevenness of a racing heartbeat, making the structure reflect the poem\'s subject directly.')],
 [('Constant (a sonnet)', (
   'The tide returns each night to claim the shore,\n'
   'A patient hand that smooths what storms have made.\n'
   'It does not rush, nor linger evermore,\n'
   'But comes and goes as promises are paid.\n\n'
   'I used to think that constancy meant still,\n'
   'A thing unmoved, unchanging, fixed in place.\n'
   'But watching water climb the rocky hill,\n'
   'I saw devotion has a rhythmic face.\n\n'
   'It leaves at dawn. By dusk it comes again.\n'
   'Not sameness, but a promise kept in motion —\n'
   'A love that ebbs, yet always answers when\n'
   'The moon calls out across the waiting ocean.\n\n'
   'So let my faithfulness be tidal, too:\n'
   'Not frozen still, but always coming back to you.')),
  ('What the Tide Taught Me (free verse)', (
   'I used to think\n'
   'constant meant\n'
   'the same.\n\n'
   'unmoving\n'
   'unbothered\n'
   'a rock, maybe,\n'
   'or a locked door.\n\n'
   'but the tide\n'
   'leaves.\n'
   'every day\n'
   'it leaves\n'
   'and every day\n'
   'it comes back\n'
   'not because it forgot how to stay\n'
   'but because leaving\n'
   'and returning\n'
   'is its whole shape\n\n'
   'maybe I was wrong\n'
   'about constant\n\n'
   'maybe it was never supposed to\n'
   'hold still\n\n'
   'maybe it was always supposed to\n'
   'come back'))],
 [('How many lines does the sonnet "Constant" have?','14 lines, the fixed length required of a traditional sonnet.'),
  ('Where does the sonnet\'s "turn" — the shift in idea — happen?','It shifts in the final couplet ("So let my faithfulness be tidal, too..."), where the speaker applies the tide\'s lesson to their own promise.'),
  ('What rhyme pattern can you identify in the sonnet\'s first stanza?','An alternating pattern (shore/still... made/place follows an ABAB-style structure across the quatrains, with shore/evermore and made/paid rhyming).'),
  ('How does the sonnet\'s consistent structure (fixed lines, steady rhyme) support its theme about constancy?','The poem\'s own steady, predictable form mirrors the tide\'s dependable rhythm, reinforcing the idea that constancy is patterned rather than static.'),
  ('How is the free verse poem\'s structure different from the sonnet\'s?','It has no fixed line count, rhyme scheme, or regular stanza length; its lines are short and irregular, breaking freely based on the idea rather than a set pattern.'),
  ('How does the free verse poem\'s short, broken lines ("unmoving / unbothered / a rock, maybe") affect its meaning?','The choppy, hesitant lines mimic the speaker\'s uncertain, evolving thought process as they reconsider what "constant" means.'),
  ('Both poems share the same central idea. State that shared idea in one sentence.','True constancy is not about staying perfectly still, but about reliably leaving and returning, like the tide.'),
  ('How does the sonnet\'s formal structure change how that shared idea feels, compared to the free verse version?','The sonnet\'s polished, patterned form gives the idea a formal, declarative, almost vow-like feeling, especially in the closing couplet.'),
  ('How does the free verse poem\'s loose structure change how that same idea feels?','It feels more like a private, in-progress realization — tentative and exploratory ("maybe I was wrong") rather than a finished declaration.'),
  ('Why might the free verse poet choose one-word or two-word lines like "constant" and "the same" instead of a full sentence?','The fragmented lines slow the reader down and emphasize each word individually, mimicking the speaker\'s piece-by-piece rethinking of the idea.'),
  ('What effect does the sonnet\'s rhyme create in the line pair "still / hill" that free verse does not attempt?','The rhyme links the two ideas (unmoving stillness and the moving tide climbing the hill) musically, reinforcing their contrast in a way free verse\'s unrhymed lines do not.'),
  ('Identify the sonnet\'s closing couplet and explain its structural role.','"So let my faithfulness be tidal, too: / Not frozen still, but always coming back to you" — it delivers the poem\'s final resolution in a rhymed pair, a structural feature specific to sonnets that signals closure.'),
  ('Does the free verse poem have an equivalent "closing couplet" moment? Explain.','No; it ends with an open, unrhymed thought ("maybe it was always supposed to / come back"), reflecting free verse\'s lack of a required closing structure, which keeps the ending feeling more open than resolved.'),
  ('How does stanza length differ between the two poems, and what effect does that have?','The sonnet uses three even quatrains plus a couplet, creating a balanced, orderly feeling; the free verse poem uses irregular, uneven stanza lengths, creating a more spontaneous, thinking-aloud feeling.'),
  ('Which poem\'s structure would you say fits its theme more literally — the fixed and returning sonnet form, or the loose, evolving free verse form? Justify your choice.','Answers vary; accept either poem if supported — for example, the sonnet\'s fixed, repeating structure literally mirrors the tide\'s reliable pattern, while free verse\'s irregular but self-returning quality can also be argued to mirror the tide\'s leaving-and-returning nature.'),
  ('How might reading the sonnet aloud change your understanding of its structure compared to reading the free verse poem aloud?','The sonnet\'s rhyme and rhythm create a musical, flowing sound when read aloud, while the free verse poem\'s short lines create pauses and a more halting, thoughtful rhythm.'),
  ('Explain how form contributes to meaning using one specific structural feature from the sonnet.','Answers vary; require a specific structural feature (rhyme scheme, the volta/turn, line count) and an explanation of how it shapes the poem\'s meaning, not just a description of the feature.'),
  ('Explain how form contributes to meaning using one specific structural feature from the free verse poem.','Answers vary; require a specific structural feature (line breaks, lack of rhyme, stanza irregularity) and an explanation of how it shapes the poem\'s meaning.'),
  ('If the free verse poem\'s ideas were forced into a strict sonnet form, what might be lost?','The hesitant, exploratory feeling created by its irregular lines and pauses might be lost, since a sonnet\'s fixed structure would impose more order and finality on what is currently an unfolding realization.'),
  ('Write a short paragraph comparing how the two forms shape the same theme differently.','Answers vary; require a clear comparison naming at least one structural difference (rhyme, line length, stanza pattern) and explaining how each form changes the reader\'s experience of the shared theme.')],
 550)

# ---------------------------------------------------------------- RL.7.6
add('rl76-character-perspectives','Character Perspectives','RL.7.6',
 'Analyze how an author develops and contrasts the perspectives of different characters in a text.',
 'Analyze how the author develops and contrasts the perspectives of two characters by examining what each character does, says, and thinks.',
 'Perspective is how a character sees and understands events, shaped by their own values, worries, or history. Authors contrast perspectives by showing two characters reacting differently to the same situation. Look at dialogue, actions, and described thoughts to understand each character\'s view.',
 [('Two characters watch a building get demolished. One says "finally," and one goes quiet. What does this contrast suggest?','It suggests one character is relieved or wanted the change, while the other may feel loss or sentimental attachment — the same event affects them differently based on their perspective.'),
  ('If a character\'s internal thought contradicts what they say aloud, what does that reveal?','It reveals a gap between their true feelings and what they are willing to express, often showing complexity or hidden concern.')],
 [('Two Directors', (
   '1. Rosario and Gerald had co-directed the Willow Street community garden for six years, an arrangement that mostly worked because they rarely needed to agree on anything at once.\n\n'
   '2. When the city offered a grant to renovate the garden\'s irrigation system, Rosario read the proposal twice and began making a list of which plots would need to be temporarily closed. Gerald read it once and immediately started drafting an email suggesting they expand the garden\'s footprint while they had the funding\'s attention.\n\n'
   '3. "We should ask for exactly what fixes the pipes," Rosario said at their next meeting, sliding her plot-closure list across the table. "If we ask for more, we risk delaying approval, and half our plots already flood every spring."\n\n'
   '4. Gerald frowned at the list without picking it up. "If we only ask for pipe repair, we\'ll be back here in three years asking for the same grant, except the expansion opportunity will be gone. Funding windows like this don\'t stay open."\n\n'
   '5. Rosario thought about the eleven families currently waiting for a plot, families she had personally told "next season, we hope," more than once. Gerald thought about the eight additional plots an expansion could create, and the families he could stop turning away permanently.\n\n'
   '6. "We\'re both trying to help the same people," Rosario finally said, more to herself than to him. "We\'re just trying to help them on different timelines."\n\n'
   '7. Gerald looked at her plot-closure list again, this time actually reading it. "Your list assumes we get denied if we ask for too much." "Your email assumes we get denied if we ask for too little," Rosario said.\n\n'
   '8. Neither of them was fully right. In the end, they submitted a proposal requesting the pipe repair with a modest, clearly justified expansion of two plots — Rosario\'s caution shaping the ask, Gerald\'s ambition shaping its size.'))],
 [('What explicit action does Rosario take first when she receives the grant proposal?','She reads it twice and begins making a list of which plots would need to be temporarily closed.'),
  ('What explicit action does Gerald take first when he receives the same proposal?','He reads it once and starts drafting an email suggesting they expand the garden\'s footprint.'),
  ('What does Rosario\'s immediate focus on plot closures suggest about her perspective?','She is cautious and focused on practical, immediate risks (like flooding and disruption) rather than opportunity.'),
  ('What does Gerald\'s immediate focus on expansion suggest about his perspective?','He is opportunity-focused and future-oriented, more willing to take a risk to achieve a larger long-term gain.'),
  ('What reason does Rosario give in paragraph 3 for asking only for pipe repair?','Asking for more risks delaying approval, and half the plots already flood every spring.'),
  ('What reason does Gerald give in paragraph 4 for wanting to expand now?','If they only ask for pipe repair, they will need to seek the same grant again in three years, but the expansion opportunity and funding window may not still be available.'),
  ('Both characters are worried about the same families. What is different about how each character thinks about those families? Cite paragraph 5.','Rosario thinks about the eleven families currently waiting and her promises to them ("next season, we hope"); Gerald thinks about the eight additional plots an expansion could create for families he is turning away, focusing on a future solution rather than the current wait.'),
  ('What does Rosario\'s statement in paragraph 6 ("We\'re just trying to help them on different timelines") reveal about her understanding of the conflict?','She recognizes that she and Gerald share the same goal but differ in urgency and approach, showing a moment of perspective-taking rather than blame.'),
  ('How does paragraph 7 show each character finally considering the other\'s viewpoint?','Gerald actually reads Rosario\'s list for the first time, and both point out the underlying assumption in the other\'s plan (that asking for too much or too little risks denial), showing mutual recognition.'),
  ('What is Rosario\'s underlying assumption, according to Gerald\'s comment in paragraph 7?','That asking for too much in the grant proposal risks getting the whole request denied.'),
  ('What is Gerald\'s underlying assumption, according to Rosario\'s comment in paragraph 7?','That asking for too little means missing the chance to solve the problem for good, since the funding opportunity may not return.'),
  ('How does the final proposal in paragraph 8 reflect both characters\' perspectives?','It includes the pipe repair Rosario prioritized for safety and urgency, plus a modest expansion reflecting Gerald\'s long-term ambition, blending both viewpoints rather than choosing one.'),
  ('Contrast Rosario\'s and Gerald\'s attitudes toward risk, using specific evidence from the story.','Rosario is risk-averse about approval delays and prioritizes a safer, smaller ask (paragraph 3); Gerald is risk-tolerant about the process but risk-averse about losing the funding opportunity itself (paragraph 4) — both avoid risk, just different kinds.'),
  ('Why might the author have chosen not to make either character clearly "right" by the end of the story?','It shows that differing, valid perspectives can both contribute something useful, and that resolving conflict does not always require one person to be wrong.'),
  ('How does the six-year co-directorship mentioned in paragraph 1 help explain their contrasting perspectives?','It shows they have different but established styles that have coexisted for years, suggesting their perspectives are long-standing traits, not new reactions to this one situation.'),
  ('Find one line of dialogue from each character that best captures their perspective, and explain your choices.','Rosario: "If we ask for more, we risk delaying approval" shows her caution; Gerald: "Funding windows like this don\'t stay open" shows his focus on long-term opportunity.'),
  ('How does the author use the described internal thoughts in paragraph 5, rather than dialogue, to develop each character\'s perspective?','By describing what each character privately thinks about the same eleven or eight families, the author shows both characters\' deeper motivations are compassionate, even though their outward approaches conflict — something dialogue alone might not reveal as clearly.'),
  ('Does the story suggest one character\'s perspective is more important to the garden\'s long-term success? Support your answer with evidence.','Answers vary; support should cite specific evidence — for example, the final compromise in paragraph 8 uses both perspectives, suggesting neither alone was sufficient, which could support an answer that both are equally necessary.'),
  ('How does the author signal, through word choice, that Rosario values caution and Gerald values opportunity, even before either character speaks?','Paragraph 2 describes Rosario making "a list of which plots would need to be temporarily closed" (careful, procedural) while Gerald "immediately" drafts an email about expansion (quick, opportunity-seeking), establishing their perspectives through action before any dialogue.'),
  ('Explain, using two pieces of evidence, how the author contrasts Rosario\'s and Gerald\'s perspectives throughout the story.','Answers vary; require two specific, correctly cited examples (from dialogue, action, or described thought) that clearly show differing viewpoints between the two characters.')],
 500)

# ---------------------------------------------------------------- RL.7.7
add('rl77-text-vs-media','Text vs. Media','RL.7.7',
 'Compare and contrast a written story, drama, or poem to its audio, filmed, staged, or multimedia version, analyzing the effects of techniques unique to each medium.',
 'Compare and contrast a written story and its film version, analyzing how techniques unique to each medium create different effects on the audience.',
 'Written stories use words to build internal thoughts, pacing, and detail directly in a reader\'s mind. Film uses techniques words cannot: camera angles, music, editing, and actors\' expressions. Comparing the two means noticing what each medium can do that the other cannot, not just what is "missing."',
 [('A written story describes a character\'s racing thoughts in a full paragraph. How might a film show the same racing thoughts without narration?','Through quick, choppy editing (fast cuts), a shaky camera, or tense background music — visual and audio techniques that suggest urgency without describing it in words.'),
  ('A film uses a slow zoom on a character\'s face during a tense moment. What is a written story\'s equivalent technique?','A written story might slow the pacing with short, deliberate sentences or describe small physical details (a held breath, a twitching hand) to build the same tension.')],
 [('The Long Second (written story)', (
   '1. Marisol had run the four hundred meters eleven times that season, and every time, the last fifty meters felt the same: her legs turning to something heavier than legs, her lungs arguing loudly with the rest of her body.\n\n'
   '2. This time was different only because it was the regional final, and because Devonte, the runner she had never beaten, was exactly one stride ahead of her with sixty meters left.\n\n'
   '3. She thought about her coach\'s voice from a hundred practices: don\'t chase the runner, chase the finish line. She thought about it for exactly as long as it took to decide it was useless advice with sixty meters left in a race this close.\n\n'
   '4. Her legs did not get lighter. Her lungs did not stop arguing. But at the twenty-meter mark, she stopped counting Devonte\'s stride and started counting her own, one two one two, until counting was the only thought left in her head.\n\n'
   '5. She crossed the line eight one-hundredths of a second before he did. She did not know this until she saw the number on the board, because for the last ten meters, she had not been able to see anything but the white line rushing toward her.\n\n'
   '6. Devonte found her afterward, both of them still catching their breath. "Eight hundredths," he said. "That\'s nothing." "It\'s not nothing," Marisol said. "It\'s the only number that matters today." He laughed, because she was right, and because there was nothing else honest to say.')),
  ('Film Scene Description: The Long Second (adapted screenplay excerpt)', (
   'EXT. TRACK — REGIONAL FINAL — DAY\n\n'
   'Wide shot: eight runners rounding the final curve. The crowd noise SWELLS. Camera cuts to MARISOL, close on her face — jaw tight, eyes locked forward.\n\n'
   'Quick cut to DEVONTE, one stride ahead. His shadow falls across Marisol\'s lane as the camera pans low, tracking their feet.\n\n'
   'The score fades out. Only footsteps and breathing remain, mixed unnaturally loud.\n\n'
   'MATCH CUT: Marisol\'s eyes, extreme close-up. A memory flash — three frames only — of her coach mid-sentence, no audio.\n\n'
   'Back to real time. The editing speeds up: quick cuts between her feet, Devonte\'s shoulder, the white finish line rushing closer, each shot shorter than the last.\n\n'
   'SLOW MOTION as she crosses the line. Sound cuts out completely for one beat.\n\n'
   'Then: the crowd roar rushes back in, full volume. Marisol doubles over, hands on knees, not looking at the board yet.\n\n'
   'CUT TO: the scoreboard. HOLD for two full seconds before Marisol turns to see it.'))],
 [('What internal detail from paragraph 3 of the written story does the film represent as a memory flash instead?','Her coach\'s advice, "don\'t chase the runner, chase the finish line" — the written story explains it in full sentences, while the film shows it as a brief, silent memory flash.'),
  ('Why might the film choose a silent, three-frame memory flash instead of dialogue for the coach\'s advice?','It preserves the scene\'s tension and pace, since stopping for spoken dialogue mid-race would break the urgency the fast editing is building.'),
  ('What technique does the film use to represent Marisol\'s narrowed focus that the written story achieves through counting ("one two one two")?','Quick, shortening cuts between her feet, Devonte\'s shoulder, and the finish line — the increasing edit speed visually mimics narrowing, intensifying focus.'),
  ('How does the written story build tension using sentence length and structure in paragraph 4?','It uses short, repeated phrases ("Her legs did not get lighter. Her lungs did not stop arguing.") and ends with the simple repetition "one two one two," mirroring urgency through pacing rather than visuals.'),
  ('What film technique described in the scene mirrors that same building tension?','The increasingly fast cuts and shortening shot lengths near the finish line mirror the same rising urgency the prose builds through short sentences.'),
  ('How does the written story convey that Marisol could not see anything but the finish line (paragraph 5)?','It states directly: "she had not been able to see anything but the white line rushing toward her."'),
  ('What specific film technique conveys a similar narrowed perception?','The slow motion during the finish line crossing, combined with sound cutting out completely for one beat, isolates that single visual and moment for the audience.'),
  ('Why is a technique like "sound cutting out" unique to film and not something a written story can literally do?','Written stories cannot remove sound because they contain no sound at all; instead, they must describe silence or a lack of awareness using words, which creates a different kind of effect.'),
  ('How does the written story handle the moment Marisol learns she won, compared to the film scene?','The written story explains it after the fact — "She did not know this until she saw the number on the board" — using retrospective narration, while the film holds on the scoreboard for two full seconds before showing Marisol\'s reaction, building suspense visually in real time.'),
  ('Which version creates more suspense about the race\'s outcome for its audience, and why?','Answers vary; a reasonable case can be made either way — the written story\'s retrospective phrasing already implies she found out something, while the film\'s held shot on the scoreboard creates real-time suspense for the viewer.'),
  ('What does the written story include after the race (paragraph 6) that the film excerpt does not show?','The full dialogue between Marisol and Devonte about "eight hundredths" and what it means, which is described in the written story but is not part of the provided film scene description.'),
  ('Why might a screenwriter still choose to include that same dialogue scene in a later part of the film, even though it works differently on screen?','Actors\' tone, facial expressions, and pauses could add layers (uncertainty, respect, humor) that the written dialogue alone conveys through described reactions like "he laughed."'),
  ('How does camera movement described in the scene ("panning low, tracking their feet") do work that the written story instead does with description?','The written story describes the physical feeling of running (heavy legs, arguing lungs) in words, while the camera pan shows the physical action of the runners\' feet directly to the viewer.'),
  ('What effect does removing the crowd noise ("the score fades out... only footsteps and breathing remain") have on the audience, compared to the written story\'s equivalent moment?','It isolates the audience\'s attention on Marisol\'s physical effort, similar to how the written story narrows focus onto her counting, but the film achieves it through sound design instead of narrated thought.'),
  ('Identify one technique unique to the written medium (something film cannot easily replicate) used in this story.','Direct access to Marisol\'s internal thoughts, like her private decision that her coach\'s advice was "useless advice with sixty meters left" — this interior reasoning is stated directly in prose in a way film usually has to imply through action or voiceover.'),
  ('Identify one technique unique to the film medium (something the written story cannot literally do) used in this scene.','The "sound cuts out completely for one beat," a literal audio technique only available in a medium that has sound.'),
  ('How do both versions still successfully convey the same core emotional experience, despite using different tools?','Both build increasing tension and narrowed focus as the race nears its end, then release that tension at the finish line — the written story through pacing and repetition, the film through editing speed and sound design.'),
  ('Compare how each medium represents the passage of "the long second" referenced in the title.','The written story slows this moment with detailed internal narration across two full paragraphs; the film represents it using slow motion and a sound cutout, both techniques designed to stretch a brief moment for the audience.'),
  ('If you were adapting the post-race dialogue scene (paragraph 6) into a film shot, what one technique would you use and why?','Answers vary; require a specific film technique (close-up, pause, music cue, etc.) and a clear explanation of how it would convey the same meaning as the written dialogue.'),
  ('Write two or three sentences comparing one technique from each medium and its specific effect on the audience.','Answers vary; require one clearly identified technique from the written story, one from the film scene, and an explanation of each one\'s specific effect, not just a general statement that they are "different."')],
 600)

# ---------------------------------------------------------------- RL.7.9
add('rl79-fiction-vs-history','Fiction vs. History','RL.7.9',
 'Compare and contrast a fictional portrayal of a time, place, or character and a historical account of the same period as a means of understanding how authors of fiction use or alter history.',
 'Compare a fictional story and a historical account of the 1960 Greensboro sit-ins, identifying what the author kept accurate, what was altered, and why those choices affect meaning.',
 'Historical fiction blends real events with invented characters and details. Authors often keep the broader facts (dates, outcomes, key events) accurate while inventing personal details (a character\'s private thoughts, an imagined conversation) to help readers connect emotionally with history.',
 [('A historical fiction story about the Titanic invents a friendship between two passengers who never actually met. Why might an author do this?','To give readers a personal, emotional entry point into a large historical event, making the scale of the disaster feel individual and relatable.'),
  ('If a historical account states a battle "lasted three days" and a novel about it says "the fighting seemed endless," is the novel wrong?','Not necessarily wrong — it is using figurative, emotional language to convey a character\'s experience, while the historical account uses precise, factual language.')],
 [('The Counter (historical fiction)', (
   '1. Etta had walked past the Woolworth\'s lunch counter every day on her way to the library for two years without once considering sitting down at it. On the first of February, she did.\n\n'
   '2. She was not one of the four young men everyone would later talk about — the ones from the college a few blocks over, who had planned it, who had worn their good clothes for it. Etta was fifteen, and she had simply seen them sitting there through the window and, without deciding to, walked in and sat two stools away.\n\n'
   '3. The woman behind the counter looked at her for a long moment, then at the four young men, then went back to wiping a spot on the counter that did not need wiping.\n\n'
   '4. Etta had expected to feel brave. Instead she felt her hands shaking, and she pressed them flat against her knees under the counter so no one could see.\n\n'
   '5. Nobody served them that day. Nobody served them the second day, either, when Etta came back, or the days after that, when the four students returned with more students each morning, filling nearly every stool.\n\n'
   '6. Etta\'s mother found out on the third day, from a neighbor, and was furious in the specific way mothers are furious when they are actually afraid. "You could have told me," she said. Etta said she hadn\'t decided to do it until she was already sitting down, which was true, and did not make her mother less afraid.\n\n'
   '7. By the end of the month, the sit-ins had spread to other cities. Etta did not know, sitting at that counter in February, that any of that would happen. She only knew that she had walked past the counter for two years, and on that particular day, she had stopped walking past it.')),
  ('February 1, 1960: The Greensboro Sit-In (historical account)', (
   'On February 1, 1960, four Black college students — Ezell Blair Jr., Franklin McCain, Joseph McNeil, and David Richmond, all freshmen at North Carolina Agricultural and Technical State University — sat down at the whites-only lunch counter at the F.W. Woolworth store in Greensboro, North Carolina. They ordered coffee and were refused service, but they remained seated until the store closed.\n\n'
   'The four students returned the next day with more classmates. By February 5, roughly three hundred students were participating, filling nearly every seat at the lunch counter and spilling into the aisles. The protest was part of a broader sit-in movement that spread rapidly: within two months, similar sit-ins had occurred in over fifty cities across the American South.\n\n'
   'The Greensboro sit-ins did not end segregation immediately. Woolworth\'s lunch counter was not formally desegregated until July 25, 1960, nearly six months after the initial protest, following months of continued demonstrations and a decline in the store\'s sales. The event is widely credited with helping to launch a wave of student-led nonviolent direct action across the country, contributing to the broader civil rights movement of the 1960s.'))],
 [('What explicit historical fact does the historical account give that the fictional story does not?','The exact date (February 1, 1960), the four students\' real names, and the exact university (North Carolina A&T) — the fiction refers to them only as "four young men" from "the college a few blocks over."'),
  ('Why might the author of the fiction story choose not to name the four real students?','To keep the story\'s focus on the invented character Etta and her personal experience, rather than retelling the documented actions of the real historical figures.'),
  ('What invented character does the fiction add that does not appear in the historical account?','Etta, the fifteen-year-old girl who joins the sit-in on the first day.'),
  ('Why might the author invent a character like Etta rather than only writing about the four real students?','To give readers a relatable, personal perspective on a large historical event — an invented character\'s private feelings (fear, impulse) can be explored freely, unlike a real historical figure\'s documented actions.'),
  ('Does the historical account state how many days passed before the lunch counter was desegregated? What is the number?','Yes — nearly six months, with the exact date given as July 25, 1960, compared to the February 1 start.'),
  ('How does the fiction story handle that same span of time?','It does not mention the eventual desegregation date at all; it ends within the same month, with Etta reflecting on the sit-in\'s early spread to other cities.'),
  ('Why might the fiction story end earlier than the full historical timeline?','Ending closer to the story\'s emotional climax (Etta\'s decision and its immediate impact) keeps the fiction focused and personal rather than trying to summarize the entire six-month outcome.'),
  ('What explicit number does the historical account give for participants by February 5?','Roughly three hundred students.'),
  ('How does the fiction story represent that same growth in participation, using different, less precise language?','It says the four students "returned with more students each morning, filling nearly every stool," giving a general impression of growth without a specific number.'),
  ('Is Etta\'s mother\'s reaction in paragraph 6 something the historical account confirms happened to any real participant? Explain.','No — the historical account does not mention individual families\' reactions at all; this is an invented detail added by the fiction to explore a personal, emotional consequence of participating.'),
  ('Why is it reasonable for the fiction to invent a detail like a parent\'s reaction, even though it is not confirmed by the historical record?','It is a plausible, realistic consequence of the real event that helps readers understand the personal risk and emotional stakes participants likely faced, even if this specific reaction was not documented for a specific person.'),
  ('What historical detail about the protest\'s spread does the historical account confirm with a specific number?','Sit-ins spread to over fifty cities within two months.'),
  ('How does the fiction story reference this same spread, and how is its treatment different?','Paragraph 7 says "the sit-ins had spread to other cities" by the end of the month, using vaguer language and a shorter, less precise timeframe than the historical account\'s specific "fifty cities" and "two months."'),
  ('Identify one core fact both texts agree on.','Both agree the sit-in began at a Woolworth\'s lunch counter, that the original participants were refused service, and that participation grew significantly within days.'),
  ('Why is it important that historical fiction keep core facts like this accurate, even while inventing characters?','It maintains the reader\'s trust that the story reflects a real event honestly, while still allowing room for emotional or personal storytelling through invented details.'),
  ('How does the historical account\'s tone differ from the fiction\'s tone?','The historical account is factual, objective, and reports events with dates and numbers; the fiction is personal and emotional, focused on Etta\'s internal feelings, like her shaking hands.'),
  ('What might a reader learn from the fiction story that the historical account does not directly provide?','A sense of the personal fear, uncertainty, and impulsive decision-making an ordinary participant might have experienced, which the historical account\'s factual style does not capture.'),
  ('What might a reader learn from the historical account that the fiction story does not directly provide?','The full scope and outcome of the protest, including exact dates, real participants\' names, and its national impact — details the fiction intentionally leaves out or generalizes.'),
  ('Explain one way the fiction story "uses" history (keeps it accurate) and one way it "alters" or adds to history (invents beyond the record).','Uses: it accurately keeps the location (Woolworth\'s lunch counter), the real students\' initial action, and the pattern of growing participation. Alters: it invents Etta, her personal fear, and her mother\'s reaction, none of which are part of the documented historical record.'),
  ('Why is it useful to compare a fictional portrayal of history to a factual account, rather than only reading one or the other?','Comparing both helps readers understand which parts of a story are verified historical fact and which are the author\'s invention, giving a fuller, more critical understanding of how history is represented in art.')],
 600)

print('Defined', len(ROWS), 'RL rows so far')
