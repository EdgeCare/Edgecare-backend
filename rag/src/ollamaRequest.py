import requests
import json
import re

OLLAMA_SERVER_URL = 'http://127.0.0.1:11434'

def modelOutput(qustion):
    return getformatedAnswer(send_prompt(qustion))

def getformatedAnswer(answer):
    prompt = '''Organize the following paragraph in a json formatted as Dict{"step_by_step_thinking": Str(explanation), "answer_choice": Str{A/B/C/...}}. please don't use any other words for punctuations. ''' + answer +'''start the response with "Here is the JSON output:" '''
    ans = send_prompt(prompt)
    ans = ans.replace("Here is the JSON output:","")
    return ans

def send_prompt(prompt):
    url = f'{OLLAMA_SERVER_URL}/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
        'model': 'llama3:8b-instruct-q8_0',
        'prompt': prompt,
        'options': {
            'temperature': 0.5,
            'max_tokens': 100
        }
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
    fullAnswer =''
    started = False
    if response.status_code == 200:
        try:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')  # Decode the line
                    json_obj = json.loads(decoded_line)  # Load JSON object
                    # print(json_obj.get('response', ''), end='')
                    
                    started = True
                    if(started == True):
                        fullAnswer += json_obj.get('response', '')
            # ansfullAnswer,explanation = format_response_v2(fullAnswer)
            return fullAnswer

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print(f"Request failed with status {response.status_code}: {response.text}")

# Example usage
# if __name__ == '__main__':
#     prompt = '''[{'role': 'system', 'content': 'You are a helpful medical expert, and your task is to answer a multi-choice medical question using the relevant documents. Please first think step-by-step and then choose the answer from the provided options. Organize your output in a json formatted as Dict{"step_by_step_thinking": Str(explanation), "answer_choice": Str{A/B/C/...}}. Your responses will be used for research purposes only, so please have a definite answer.'}, {'role': 'user', 'content': "\nHere are the relevant documents:\nDocument [0] (Title: InternalMed_Harrison) As with any treatment recommendation, the risks and benefits of adjuvant chemotherapy should be considered on an individual patient basis. If a decision is made to proceed with adjuvant chemotherapy, in general, treatment should be initiated 6–12 weeks after surgery, assuming the patient has fully recovered, and should be administered for no more than four cycles. Although a cisplatinbased chemotherapy is the preferred treatment regimen, carboplatin can be substituted for cisplatin in patients who are unlikely to tolerate cisplatin for reasons such as reduced renal function, presence of neuropathy, or hearing impairment. No specific chemotherapy regimen is considered optimal in this setting, although platinum plus vinorelbine is most commonly used.\nDocument [1] (Title: Neurology_Adams) This has many causes. The common high-frequency sensorineural type of hearing loss in the aged (presbycusis) is probably a result of neuronal degeneration, that is, progressive loss of spiral ganglion neurons (Suga and Lindsay). Explosions or intense, sustained noise in certain industrial settings or from gun blasts or even rock music may result in a high-tone sensorineural hearing loss from cochlear damage. Certain antimicrobial drugs (namely, the aminoglycoside group and vancomycin) damage cochlear hair cells and, after prolonged use, can result in severe hearing loss. If these drugs have been used to treat bacterial meningitis, it may be difficult to determine whether the antibiotic or the infection is the cause. A variety of other commonly used drugs are ototoxic, including certain neurotoxic cancer chemotherapies, especially platinum containing drugs, usually in a dose-dependent fashion (see Nadol). Quinine and acetylsalicylic acid may impair sensorineural function transiently.\nDocument [2] (Title: InternalMed_Harrison) Vinca alkaloids produce a characteristic “stocking-glove” neuropathy with numbness and tingling advancing to loss of motor function, which is highly dose related. Distal sensorimotor polyneuropathy prominently involves loss of deep tendon reflexes with initially loss of pain and temperature sensation, followed by proprioceptive and vibratory loss. This requires careful patient history and physical examination by experienced oncologists to decide when the drug must be stopped due to toxicity. Milder toxicity often slowly completely resolves. Vinca alkaloids may sometimes be associated with jaw claudication, autonomic neuropathy, ileus, cranial nerve palsies, and, in severe cases, encephalopathy, seizures, and coma. Cisplatin is associated with sensorimotor neuropathy and hearing loss, especially at doses >400 mg/m2, requiring audiometry in patients with preexisting hearing compromise. Carboplatin is often substituted in such cases given its lesser effect on hearing.\nDocument [3] (Title: InternalMed_Harrison) (or vestibular toxicity with streptomycin) is not uncommon during treatment lasting 4–6 weeks. Regimens in which the aminoglycoside component is given for only 2–3 weeks have been curative and associated with less nephrotoxicity than those using longer courses of gentamicin. Thus regimens wherein gentamicin is administered for only 2–3 weeks are preferred by some.\nDocument [4] (Title: InternalMed_Harrison) A number of chemotherapeutic drugs have activity as single agents; cisplatin, paclitaxel, and gemcitabine are considered most active. Standard therapy consists of two-, three-, or four-drug combina tions. Overall response rates of >50% have been reported using combinations such as methotrexate, vinblastine, doxorubicin, and cisplatin (MVAC); gemcitabine and cisplatin (GC); or gemcitabine, paclitaxel, and cisplatin (GPC). MVAC was considered standard, but the toxicities of neutropenia and fever, mucositis, diminished renal and auditory function\n\nHere is the question:\nA 67-year-old man with transitional cell carcinoma of the bladder comes to the physician because of a 2-day history of ringing sensation in his ear. He received this first course of neoadjuvant chemotherapy 1 week ago. Pure tone audiometry shows a sensorineural hearing loss of 45 dB. The expected beneficial effect of the drug that caused this patient's symptoms is most likely due to which of the following actions?\n\nHere are the potential choices:\nA. Inhibition of proteasome\nB. Hyperstabilization of microtubules\nC. Generation of free radicals\nD. Cross-linking of DNA\n\nPlease think step-by-step and generate your output in json:\n"}]'''
    
    
#     send_prompt(prompt)


def format_response_v2( model_response):
    """
    Formats the model response to match the specified JSON output:
    {"step_by_step_thinking": Str(explanation), "answer_choice": Str{A/B/C/...}}
    """
    answer_choice, explanation = extract_answer_rationale(model_response)
    
    formatted_output = {
        "step_by_step_thinking": explanation,
        "answer_choice": answer_choice
    }
    return formatted_output

def extract_answer_rationale(raw_text):
    """
    Extracts the answer choice and explanation from a variable format output.
    Falls back to default messages if extraction fails.
    """
    # Initialize placeholders for answer and explanation
    answer_choice = "N/A"
    explanation = "Explanation not found."

    # Attempt to find answer choice with common patterns
    answer_match = re.search(r"The correct answer is ([A-D])", raw_text)
    if not answer_match:
        answer_match = re.search(r"answer_choice", raw_text)
    
    if answer_match:
        answer_choice = answer_match.group(1)
    else:
        # Fallback if no pattern match for answer
        fallback_answer_match = re.search(r"\b([A-D])\b", raw_text)
        if fallback_answer_match:
            answer_choice = fallback_answer_match.group(1)

    # Attempt to find explanation with common patterns
    explanation_match = re.search(r"Explanation: (.+)", raw_text)
    if explanation_match:
        explanation = explanation_match.group(1)
    else:
        # Try alternative keywords if "Explanation:" is missing
        rationale_match = re.search(r"Reason: (.+)", raw_text) or re.search(r"Because: (.+)", raw_text)
        if rationale_match:
            explanation = rationale_match.group(1)
        else:
            # Fallback to capturing a general description if patterns fail
            description_match = re.search(r"(.+)", raw_text)
            if description_match:
                explanation = description_match.group(1)
    
    return answer_choice, explanation