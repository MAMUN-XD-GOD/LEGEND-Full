import zipfile, os
BATCH_DIRS = ['quantum_apex_batch1_final','quantum_apex_batch2_final','quantum_apex_batch3_final','quantum_apex_batch4_final','quantum_apex_batch5_final','quantum_apex_batch6_final','quantum_apex_batch7_final']
OUT='quantum_apex_full_combined.zip'
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as out:
    for d in BATCH_DIRS:
        if not os.path.exists(d):
            print('Missing', d)
            continue
        for root,_,files in os.walk(d):
            for f in files:
                full = os.path.join(root,f)
                arc = os.path.join(os.path.basename(d), os.path.relpath(full,d))
                out.write(full, arc)
print('Created', OUT)
