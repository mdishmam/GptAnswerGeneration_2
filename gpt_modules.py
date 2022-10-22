import openai

keys_fl = open('openai_credentials.txt','r')
keys = keys_fl.readlines()
keys_fl.close()

if '' in keys:
    keys.remove('')
key = keys[0].strip()

openai.api_key = key

def write_intro_1_text(keyword,temp=0.7):
    prompt = f"write a introduction for the following topic: \"{keyword}\"\n\n"
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=temp,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print('\t\tintro1 done.\n\n')
    intro_1 = response.choices[0].text

    return intro_1

def write_intro_2_text(keyword,temp=0.7):
    prompt = f"write exact ans for the following topic: \"{keyword}\"\n\n"
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=temp,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print('\t\tintro2 done.\n\n')
    intro_2 = response.choices[0].text

    return intro_2

def write_intro(keyword, temp= 0.7):
    intro_1 = write_intro_1_text(keyword, temp)
    intro_2 = write_intro_2_text(keyword, temp)
    intro = intro_1 + '<br><br>' + intro_2
    return intro

def rewrite_text(text, temp=0.7):
    prompt = f"write a note on following topic:\n{text}\n\n"
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=temp,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print('\t\trewite done.\n\n')
    output = response.choices[0].text

    return output