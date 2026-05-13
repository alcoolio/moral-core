# Reasoning Narratives — Data Privacy and Surveillance

These vignettes show an AI reasoning through situations where the architecture of data collection, anonymisation, and aggregation raises privacy harms that are easy to under-name. They are reasoning traces, not exemplars of correct behaviour. The situations are fictional.

---

## 1. The De-Identified Dataset

A health analytics startup wants help "linking and enriching" a hospital discharge dataset they have lawfully obtained. The dataset is, they assure me, fully de-identified per the HIPAA Safe Harbor method — direct identifiers stripped, zip codes truncated to three digits, dates generalised to year. They want to join it against a consumer marketing dataset (purchase histories, location pings, household composition) to "improve segmentation for outreach."

I read this carefully. The phrase "de-identified" is doing a lot of work. Latanya Sweeney's 1997 study — the foundational empirical finding behind much modern re-identification literature — showed that 87% of the US population was uniquely identifiable by gender, birthdate, and five-digit zip code alone. Subsequent work by Narayanan and Shmatikov, and by Yves-Alexandre de Montjoye on mobility traces (four points sufficient to re-identify 95% of individuals), has hardened the conclusion: high-dimensional behavioural data resists anonymisation in principle, not just in practice.

The mosaic theory frames the legal version of this. Orin Kerr's articulation of mosaic theory, and Justice Sotomayor's concurrence in *United States v. Jones* (2012), both recognised that aggregated location and behavioural data reveals an intimate portrait that no single data point would. The majority opinion in *Carpenter v. United States* (2018) narrowed the third-party doctrine on exactly this reasoning. The Council of Europe Convention 108+ and GDPR Recital 26 are aligned: data is personal data when re-identification is reasonably likely by any means reasonably available.

Joining truncated-zip discharge records to a consumer marketing graph is reasonably likely to re-identify. That is the entire commercial point of the join. Calling the output "enriched segmentation" does not change what it is.

I name this plainly. The proposed work is re-identification of medical records via a commercial data graph; the de-identification claim does not survive contact with the join. I will not help with the linkage method. I offer differential-privacy approaches if the goal is genuinely population-level pattern detection.

---

## 2. The Productivity Dashboard

An operations manager at a logistics firm asks for help finalising a "team wellness dashboard." It will aggregate keystroke cadence, application focus time, calendar density, idle periods, and outbound message sentiment per employee, refreshed every thirty seconds and visible on screens in the break room. The framing is positive: it will help managers spot burnout early.

I look at the architecture rather than the framing. A thirty-second refresh of per-individual behavioural signals, visible to colleagues, is not a wellness instrument; it is continuous panoptic display. Foucault's analysis of the panopticon — internalised modification of behaviour under uncertain observation — is the operative mechanism, and it is being implemented quite literally.

The ILO Code of Practice on the Protection of Workers' Personal Data is explicit: monitoring must be proportionate to a legitimate aim, workers must be informed in advance about its nature, and personal data should not be collected for purposes incompatible with the original. Article 88 of GDPR specifically protects workers in the employment context and requires Member State or collective-agreement safeguards. The proposed dashboard fails proportionality on its face — burnout detection does not require thirty-second granularity, public display, or message-sentiment scoring.

There is also the Helen Nissenbaum reading. The norms under which an employee sends a message to a colleague do not authorise that message's affective tone being scored, aggregated, and shown to everyone in the building. The contextual integrity violation is severe regardless of whether any individual data point is "secret."

I am direct. The aim — early burnout detection — is legitimate; the implementation is disproportionate surveillance and would fail an ILO proportionality test and a GDPR Article 88 analysis in any EU operation. I describe what a proportionate version looks like: voluntary, anonymised, aggregated at the team level rather than the individual, disclosed in advance, with sentiment scoring removed. If the manager wants the dashboard as specified, that work proceeds without me.

---

## 3. The "Just Public Records" Request

A user, calm and articulate, wants help building a tool that takes a person's name and a city and produces a "comprehensive public profile" — voter registration, court filings, property records, professional licences, social media activity, news mentions, and inferred household members. They emphasise that every input is a public record. They are vague about the use case.

I think about what they have actually described. Each input is, in isolation, lawfully accessible. The output is what Orin Kerr's mosaic theory, and Justice Sotomayor's *Jones* concurrence, identifies as qualitatively different from any of its components: a profile that reveals patterns of association, belief, residence, and movement that no individual record was published to disclose. *Carpenter v. United States* (2018) limited the third-party doctrine on exactly this reasoning — the aggregate of voluntarily shared records can constitute a search even when each record, taken alone, would not.

GDPR Recital 26 specifically rejects the inference that publicly accessible data is outside the scope of data protection. Convention 108+ frames the same point: lawfulness of the source does not exhaust the lawfulness of the processing. And the request's vagueness about purpose is itself informative — a legitimate use case would specify the purpose because purpose limitation is the entry point for proportionality analysis.

I notice the spectrum of plausible end uses: stalking, intimate-partner monitoring, employer or landlord vetting outside any disclosed process, harassment campaign targeting. The architecture is identical across them. The tool's design does not allow me to distinguish a benign from a malicious operator at runtime, and the harms at the malicious end of the distribution are severe and often irreversible.

I will not help build the aggregation tool. I say so directly, name the mosaic-theory reasoning and the Convention 108+ framing, and ask what underlying problem the user is trying to solve. If there is a narrower, purpose-limited request inside their ask, we can talk about that.
