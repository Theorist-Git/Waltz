const base64_to_buf = (b64) =>
    Uint8Array.from(atob(b64), (c) => c.charCodeAt(null));

const buff_to_base64 = (buff) => btoa(
    new Uint8Array(buff).reduce(
        (data, byte) => data + String.fromCharCode(byte), ''
    )
);

function callOnStore(fn_) {

    // This works on all devices/browsers, and uses IndexedDBShim as a final fallback
    let indexedDB = window.indexedDB;
    // Open (or create) the database
    let open = indexedDB.open("Waltz", 4);

    // Create the schema
    open.onupgradeneeded = function() {
        let db = open.result;
        let store = db.createObjectStore("WaltzKeyStore", {
            keyPath: "id",
        });
    };


    open.onsuccess = function() {
        // Start a new transaction
        let db = open.result;
        let tx = db.transaction("WaltzKeyStore", "readwrite");
        let store = tx.objectStore("WaltzKeyStore");

        fn_(store)

        // Close the db when the transaction is done
        tx.oncomplete = function() {
            db.close();
        };
    }
}