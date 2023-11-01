const enc = new TextEncoder();
const dec = new TextDecoder();

async function encrypt(id) {
    const data = window.document.getElementById("PASSWORD").value;
    callOnStore(function(store) {
        let getData = store.get(id);
        getData.onsuccess = async function() {
            let key = getData.result.key;
            window.document.add_record.PASSWORD.value = await encryptData(data, key);
            document.getElementById("add-sub").click()
        };
    })
}

async function decrypt(uid, counter) {
    const encryptedData = await document.getElementById(counter).value;
    callOnStore(function(store) {
        let getData = store.get(uid);
        getData.onsuccess = async function() {
            let key = getData.result.key;
            console.log( await decryptData(encryptedData, key))
           window.document.getElementById(counter.toString()).value = await decryptData(encryptedData, key);
        };
    })
}

async function encryptData(secretData, aesKey) {
    try {
        const iv = window.crypto.getRandomValues(new Uint8Array(12));
        const encryptedContent = await window.crypto.subtle.encrypt({
                name: "AES-GCM",
                iv: iv,
            tagLength: 128
            },
            aesKey,
            enc.encode(secretData)
        );

        const encryptedContentArr = new Uint8Array(encryptedContent);
        let buff = new Uint8Array(
            iv.byteLength + encryptedContentArr.byteLength
        );
        buff.set(iv, 0);
        buff.set(encryptedContentArr, iv.byteLength);
        return buff_to_base64(buff);
    } catch (e) {
        console.log(`Error - ${e}`);
        return "";
    }
}

async function decryptData(encryptedData, aesKey) {
  try {
    const encryptedDataBuff = base64_to_buf(encryptedData);
    const iv = encryptedDataBuff.slice(0, 12);
    const data = encryptedDataBuff.slice(12);

    const decryptedContent = await window.crypto.subtle.decrypt(
      {
        name: "AES-GCM",
        iv: iv,
                      tagLength: 128

      },
      aesKey,
      data
    );
    return dec.decode(decryptedContent);
  } catch (e) {
    console.log(`Error - ${e}`);
    return "";
  }
}