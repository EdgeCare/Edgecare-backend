from rag.src.rag import MedRAG

question = "A lesion causing compression of the facial nerve at the stylomastoid foramen will cause ipsilateral"
options = {
    "A": "paralysis of the facial muscles.",
    "B": "paralysis of the facial muscles and loss of taste.",
    "C": "paralysis of the facial muscles, loss of taste and lacrimation.",
    "D": "paralysis of the facial muscles, loss of taste, lacrimation and decreased salivation."
}
# answer A


# question= "A 67-year-old man with transitional cell carcinoma of the bladder comes to the physician because of a 2-day history of ringing sensation in his ear. He received this first course of neoadjuvant chemotherapy 1 week ago. Pure tone audiometry shows a sensorineural hearing loss of 45 dB. The expected beneficial effect of the drug that caused this patient's symptoms is most likely due to which of the following actions?"
# options= {
#                 "A": "Inhibition of proteasome",
#                 "B": "Hyperstabilization of microtubules",
#                 "C": "Generation of free radicals",
#                 "D": "Cross-linking of DNA"
#             }
# "answer": "D"

# question= "Is anorectal endosonography valuable in dyschesia?"
# options =  {
#                 "A": "yes",
#                 "B": "no",
#                 "C": "maybe"
#             }
            # "answer": "A"

# question= "A 68-year-old male comes to the physician for evaluation of right flank pain. He has a history of diabetes and peripheral artery disease. His blood pressure is 160/90 mm Hg. Physical examination shows abdominal tenderness and right flank tenderness. An ultrasound shows dilation of the right ureter and renal pelvis. Which of the following is the most likely underlying cause of this patient's condition?"
# options= {
#                 "A": "Renal artery stenosis",
#                 "B": "Benign prostatic hyperplasia",
#                 "C": "Common iliac artery aneurysm",
#                 "D": "Urethral stricture"
#             }

# answer = "C"
medrag = MedRAG(llm_name="OpenAI/gpt-3.5-turbo", rag=True, retriever_name="MedCPT", corpus_name="Textbooks")

### MedRAG without pre-determined snippets
answer, snippets, scores = medrag.answer(question=question, options=options, k=32)
print(answer)

print("done")
# ## CoT Prompting
# cot = MedRAG(llm_name="OpenAI/gpt-3.5-turbo-16k", rag=False)
# answer, _, _ = cot.answer(question=question, options=options)

# ## MedRAG
# medrag = MedRAG(llm_name="OpenAI/gpt-3.5-turbo-16k", rag=True, retriever_name="MedCPT", corpus_name="Textbooks")

# ### MedRAG without pre-determined snippets
# answer, snippets, scores = medrag.answer(question=question, options=options, k=32) # scores are given by the retrieval system

# ### MedRAG with pre-determined snippets
# snippets = [{'id': 'InternalMed_Harrison_30037', 'title': 'InternalMed_Harrison', 'content': 'On side of lesion Horizontal and vertical nystagmus, vertigo, nausea, vomiting, oscillopsia: Vestibular nerve or nucleus Facial paralysis: Seventh nerve Paralysis of conjugate gaze to side of lesion: Center for conjugate lateral gaze Deafness, tinnitus: Auditory nerve or cochlear nucleus Ataxia: Middle cerebellar peduncle and cerebellar hemisphere Impaired sensation over face: Descending tract and nucleus fifth nerve On side opposite lesion Impaired pain and thermal sense over one-half the body (may include face): Spinothalamic tract Although atheromatous disease rarely narrows the second and third segments of the vertebral artery, this region is subject to dissection, fibromuscular dysplasia, and, rarely, encroachment by osteophytic spurs within the vertebral foramina.', 'contents': 'InternalMed_Harrison. On side of lesion Horizontal and vertical nystagmus, vertigo, nausea, vomiting, oscillopsia: Vestibular nerve or nucleus Facial paralysis: Seventh nerve Paralysis of conjugate gaze to side of lesion: Center for conjugate lateral gaze Deafness, tinnitus: Auditory nerve or cochlear nucleus Ataxia: Middle cerebellar peduncle and cerebellar hemisphere Impaired sensation over face: Descending tract and nucleus fifth nerve On side opposite lesion Impaired pain and thermal sense over one-half the body (may include face): Spinothalamic tract Although atheromatous disease rarely narrows the second and third segments of the vertebral artery, this region is subject to dissection, fibromuscular dysplasia, and, rarely, encroachment by osteophytic spurs within the vertebral foramina.'}]
# answer, _, _ = medrag.answer(question=question, options=options, snippets=snippets)

# ### MedRAG with pre-determined snippet ids
# snippets_ids = [{"id": s["id"]} for s in snippets]
# answer, snippets, _ = medrag.answer(question=question, options=options, snippets_ids=snippets_ids)

