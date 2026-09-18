import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ela_deck import Deck

d = Deck('RL.7.5', 'Form, Structure & Meaning')

d.cover('GRADE 7  ·  READING LITERATURE  ·  RL.7.5', 'Form, Structure & Meaning',
        'A sonnet and a free verse poem — how the shape of a poem changes what it means',
        'Definitions  ·  Models  ·  Task Cards  ·  Passages  ·  Multiple-Choice Practice')

d.two_box('LESSON MAP', 'What You Will Learn Today',
          'Learning Goals',
          ['Name the form and structure of a poem',
           'Explain what a sonnet’s 14 lines and rhyme scheme do',
           'Explain how free verse breaks from fixed patterns',
           'Trace how form shapes a poem’s meaning and feeling',
           'Support answers with text evidence'],
          'How the Lesson Runs',
          ['Definitions with quick examples',
           'One modeled example together',
           'Three task cards for partner work',
           'Two full poems, sonnet and free verse',
           'Answer key and exit ticket'])

d.guide_note('GUIDE NOTE', 'Unpacking the Standard',
             ['RL.7.5 asks you to analyze how a poem’s form or structure contributes to its meaning — not just describe the form, but explain what it does.',
              'Form is the overall shape a poem takes (sonnet, free verse, ballad). Structure is how it is built: line length, stanza breaks, rhyme, and where the idea shifts.',
              'Two poems can share the exact same theme and still feel completely different because of the choices their form makes.'])

d.definition(1, 5, 'Form',
             'The overall type or shape a poem takes, following (or breaking) a recognized pattern.',
             'A sonnet is a form with 14 lines and a fixed rhyme scheme. Free verse is also a form — the form of having no fixed pattern.',
             'Form = the poem’s recognizable shape.')
d.definition(2, 5, 'Structure',
             'How a text is built: its line breaks, stanza lengths, rhyme pattern, and the order ideas appear in.',
             'A poem with three even stanzas and a final rhymed couplet has a very different structure than one with one long, unbroken block of lines.',
             'Structure = the specific choices that build the form.')
d.definition(3, 5, 'Sonnet',
             'A 14-line poem, traditionally with a fixed rhyme scheme and a "turn" where the idea shifts.',
             'In "Constant," the sonnet’s final two rhymed lines deliver the poem’s conclusion after three steady quatrains.',
             'Count the lines: exactly 14 signals a sonnet.')
d.definition(4, 5, 'Free Verse',
             'Poetry with no fixed rhyme scheme or line length; line breaks are chosen freely to match meaning.',
             'In "What the Tide Taught Me," one-word lines like "constant" slow the reader down on purpose — no rhyme is forcing the pace.',
             'Free verse structure is a choice, not an absence of structure.')
d.definition(5, 5, 'Volta (the turn)',
             'The point in a poem, often near the end, where its idea shifts or resolves — common in sonnets.',
             'The sonnet "Constant" turns in its final couplet: "So let my faithfulness be tidal, too."',
             'Ask: where does the poem’s thinking change?')

d.two_box('SIDE BY SIDE', 'Two Forms, One Theme',
          'Sonnet: "Constant"',
          ['14 lines, steady rhyme scheme',
           'Three quatrains build one idea',
           'Final couplet delivers the turn',
           'Feels formal, resolved, vow-like'],
          'Free Verse: "What the Tide Taught Me"',
          ['No fixed line count or rhyme',
           'Short, broken lines, irregular stanzas',
           'Ends on an open, unrhymed thought',
           'Feels private, unfinished, exploratory'])

d.guide_note('WE DO TOGETHER', 'Modeled Example: Read the Structure',
             ['A poem with a strict rhyme scheme describes a chaotic storm. What effect might that contrast create?',
              'Model answer: The poem’s orderly form pulls against its chaotic subject — it can suggest the speaker is trying to impose control on something that resists control. The contrast itself becomes part of the meaning.',
              'Now try this one: a free verse poem about a racing heartbeat uses short, irregular lines. Why might that structure fit the content? (Discuss with a partner before the next slide.)'])

d.guide_note('GUIDE NOTE', 'Sentence Starters & Signal Words',
             ['"The poem’s [rhyme scheme / line length / stanza pattern] contributes to its meaning by..."',
              '"Because the form is [fixed / free], the poem feels..."',
              '"The turn happens at [line/stanza], where the idea shifts from ___ to ___."',
              'Signal words: form, structure, stanza, line break, rhyme scheme, turn (volta), contributes to.'])

d.task_card(1, 3, 'Read the Sonnet’s Structure', 'How does the sonnet’s fixed form shape its meaning?',
            'With your partner',
            ['1. Count the sonnet’s lines and stanzas.',
             '2. Find where the poem’s idea turns.',
             '3. Underline the rhyme pairs in stanza 1.',
             '4. Write one sentence: the steady rhyme makes the poem feel ___.'],
            'Challenge',
            'Rewrite the sonnet’s final couplet as two unrhymed free-verse lines. What is lost?')

d.passage('PRACTICE PASSAGE A · PART 1', 'Passage A: "Constant" (a sonnet)',
          ['The tide returns each night to claim the shore,',
           'A patient hand that smooths what storms have made.',
           'It does not rush, nor linger evermore,',
           'But comes and goes as promises are paid.', '',
           'I used to think that constancy meant still,',
           'A thing unmoved, unchanging, fixed in place.',
           'But watching water climb the rocky hill,',
           'I saw devotion has a rhythmic face.'], size=13, space_after=10)
d.passage('PRACTICE PASSAGE A · PART 2', 'Passage A: "Constant," continued',
          ['It leaves at dawn. By dusk it comes again.',
           'Not sameness, but a promise kept in motion —',
           'A love that ebbs, yet always answers when',
           'The moon calls out across the waiting ocean.', '',
           'So let my faithfulness be tidal, too:',
           'Not frozen still, but always coming back to you.'],
          note='The poem’s turn: the final couplet applies the tide’s lesson to the speaker’s own promise.',
          size=13, space_after=10)

d.mc_questions('PRACTICE PASSAGE A', 'Passage A: Structure Check',
               [('How many lines does "Constant" have, and what form does that confirm?',
                 ['12 lines; an ode', '14 lines; a sonnet', '16 lines; a ballad', '10 lines; free verse']),
                ('Where does the poem’s "turn" happen?',
                 ['The first line', 'The final couplet', 'The title', 'It never turns']),
                ('What effect does the steady rhyme scheme create?',
                 ['A chaotic, rushed feeling', 'A formal, dependable feeling that mirrors the tide', 'No effect on meaning', 'Confusion about the speaker'])])

d.task_card(2, 3, 'Read the Free Verse’s Structure', 'How does the free verse form shape its meaning?',
            'With your partner',
            ['1. Notice the short, broken lines.',
             '2. Find a one-word or two-word line.',
             '3. Discuss why the poet chose that break.',
             '4. Write one sentence: the broken lines make the poem feel ___.'],
            'Challenge',
            'Combine three short lines into one full sentence. What changes about the poem’s feeling?')

d.passage('PRACTICE PASSAGE B · PART 1', 'Passage B: "What the Tide Taught Me" (free verse)',
          ['I used to think', 'constant meant', 'the same.', '',
           'unmoving', 'unbothered', 'a rock, maybe,', 'or a locked door.'],
          size=13, space_after=9)
d.passage('PRACTICE PASSAGE B · PART 2', 'Passage B: "What the Tide Taught Me," continued',
          ['but the tide leaves. every day it leaves,',
           'and every day it comes back —',
           'not because it forgot how to stay',
           'but because leaving and returning is its whole shape.', '',
           'maybe I was wrong about constant.',
           'maybe it was never supposed to hold still —',
           'maybe it was always supposed to come back.'],
          note='The poem never rhymes or resolves neatly — the structure stays open, matching its still-forming idea.',
          size=12, space_after=8)

d.mc_questions('PRACTICE PASSAGE B', 'Passage B: Structure Check',
               [('What is different about this poem’s structure compared to the sonnet?',
                 ['It has a strict rhyme scheme too', 'It has no fixed line count or rhyme', 'It is exactly 14 lines', 'It uses the same stanza pattern']),
                ('Why might the poet use short, one-word lines like "constant" and "the same"?',
                 ['To fill space', 'To slow the reader and emphasize each word', 'Because free verse requires short lines', 'It is a mistake']),
                ('How does the poem’s ending differ in structure from the sonnet’s ending?',
                 ['It also ends in a rhymed couplet', 'It ends on an open, unrhymed thought', 'It repeats the first line', 'It has no ending'])])

d.guide_note('GUIDE NOTE', 'Comparing the Two Forms',
             ['Both poems share the same idea: true constancy means reliably leaving and returning, like the tide — not staying perfectly still.',
              'The sonnet’s fixed structure gives that idea a formal, vow-like feeling, especially in its rhymed closing couplet.',
              'The free verse poem’s loose structure gives the same idea a private, in-progress feeling — like a thought still being worked out.'])

d.task_card(3, 3, 'Same Theme, Different Form', 'How does form change the feeling of a shared idea?',
            'With your partner',
            ['1. State the theme both poems share, in one sentence.',
             '2. Name one structural difference between them.',
             '3. Explain how that difference changes the feeling.',
             '4. Decide: which form fits the tide theme better? Defend it.'],
            'Challenge',
            'Write four free-verse lines that carry the sonnet’s final message, without rhyme.')

d.mc_questions('MIXED PRACTICE', 'Check Your Understanding (1 of 2)',
               [('What shared theme do both poems explore?',
                 ['That change is always bad', 'That true constancy means reliably leaving and returning', 'That the ocean is dangerous', 'That poems must rhyme']),
                ('Which structural feature is unique to the sonnet, not the free verse poem?',
                 ['Line breaks', 'A fixed rhyme scheme', 'Stanzas', 'Imagery about water']),
                ('Which phrase best describes the free verse poem’s effect, based on its structure?',
                 ['Formal and finished', 'Tentative and exploratory', 'Angry and rushed', 'Simple and childish'])], start=1)

d.mc_questions('MIXED PRACTICE', 'Check Your Understanding (2 of 2)',
               [('If the free verse poem were rewritten as a strict sonnet, what would most likely be lost?',
                 ['The theme about the tide', 'The hesitant, thinking-aloud feeling of the short lines', 'All rhyme', 'The title']),
                ('What is the best definition of a poem’s "turn" or volta?',
                 ['The first line of the poem', 'The point where the poem’s idea shifts or resolves', 'A word that rhymes', 'The poem’s title'])], start=4)

d.answer_key('TEACHER PAGE', 'Answer Key (1 of 2)',
             [('Passage A, Q1', 'B', '"Constant" has 14 lines, the fixed length required of a sonnet.'),
              ('Passage A, Q2', 'B', 'The turn happens in the final couplet, where the speaker applies the tide’s lesson to their own promise.'),
              ('Passage A, Q3', 'B', 'The steady, patterned rhyme mirrors the tide’s dependable rhythm, reinforcing a formal, resolved feeling.'),
              ('Passage B, Q1', 'B', 'Free verse has no fixed rhyme scheme or line count, unlike the sonnet.')])
d.answer_key('TEACHER PAGE', 'Answer Key (2 of 2)',
             [('Passage B, Q2', 'B', 'Short, isolated lines slow the reader down and emphasize each word individually.'),
              ('Passage B, Q3', 'B', 'It ends on an open, unrhymed thought, unlike the sonnet’s resolved couplet.'),
              ('Mixed 1–2', 'B / B', 'Both poems share the tide theme; only the sonnet has a fixed rhyme scheme.'),
              ('Mixed 3–5', 'B / B / B', 'Free verse feels exploratory; forcing it into a sonnet would lose that; a volta is where the poem’s idea turns.')])

d.exit_ticket('Answer on a sticky note',
              ['Pick one poem from today.',
               'In two sentences, explain one structural choice and the effect it creates.'],
              'Remember',
              ['Name the structural feature', 'Name the effect on meaning or feeling', 'Quote the evidence', 'Use a because / so that link'])

n = d.save('/home/user/saint-pierre-learning-resources/tmp/ela-build/rl7-5-form-structure.pptx')
print('Built', n, 'slides')
