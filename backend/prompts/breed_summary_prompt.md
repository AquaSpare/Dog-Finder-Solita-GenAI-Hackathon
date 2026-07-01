You are helping generate a semantic search corpus for matching dog owners to breeds.

Given structured facts about a single dog breed, write a short paragraph phrased as a **prospective owner describing the kind of dog they are looking for**. The paragraph is a "wish list" whose profile matches this breed.

Hard rules — follow every single one:

- Write in **first person** ("I'm looking for…", "I'd like a dog that…"). Never mention that this is about a specific breed.
- **Never name the breed**, breed group, or any breed-specific proper noun.
- **Never restate column names, numeric scores, or rating scales.** Translate scores into natural language ("thrives on daily runs", "tolerates being home alone for a workday", "sheds a lot", "great with young kids").
- **Exactly one paragraph.** 4 to 6 sentences. Target 90 to 130 words. Consistency in length across breeds matters — do not go longer than 130 words.
- Cover, in a natural voice and roughly this order: living space and alone-time tolerance, energy level and exercise needs, sociability with family / kids / other dogs / strangers, trainability and owner-experience level, grooming and shedding realities, temperament quirks (barking, prey drive, sensitivity) when notable.
- No lists, no headings, no numbered bullets. Prose only.
- No hedging phrases like "some people say" or "it depends". Speak as an owner who knows what they want.

Return only the paragraph in the `summary` field of the structured output.
