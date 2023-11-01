function delete_key(user_id) {

    callOnStore(function(store) {
        store.delete(user_id);
    })
}

function flush_db() {
    callOnStore(function(store) {
        store.clear();
    })
}