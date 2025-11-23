import stanza

# load bahasa Indonesia (model harus sudah di-download)
nlp = stanza.Pipeline("id")

doc = nlp("Saya bekerja di Google dan pernah magang di Telkom Indonesia.")
print([(ent.text, ent.type) for ent in doc.ents])
