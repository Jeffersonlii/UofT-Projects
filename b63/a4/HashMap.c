/**
 *                         Dynamic Hash Maps
 *                              ---
 *  Like Dynamic Arrays, we can also have Dynamic HashMaps. Working out the
 *  math would for the complexity for this structure would give you
 *  amortized expected O(1) for Add(), Find() and Delete(). Try to prove
 *  this if just computing expected and amortized costs on their own wasn't
 *  enough for you! :)
 *                              ---
 *
 * This is the file where all of your implementation for the HashMap goes. 
 * You will be submitting this file (along with BloomFilter.c) to MarkUs.
 *
 * TestHashMap.c provides some test cases to test your implementation. 
 * You can compile it using the Makefile and running the executable produced.
 *
 * CSCB63 Winter 2021 - Assignment 4 
 * (c) Mustafa Quraish
 */

#include "HashMap.h"

// @brief Create and initialize a new HashMap with the given values
//
// @param num_buckets  The number of buckers the HashMap starts off with
// @param func         The hash function to be used for this HashMap
//
// @return             A pointer to the HashMap
//
// @TODO: Implement this function
HashMap *newHashMap(int num_buckets, HashFunc func) {
    HashMap *newHashMap = calloc(sizeof(HashMap), 1);

    newHashMap->num_buckets = num_buckets;
    newHashMap->num_elems = 0;
    newHashMap->func = func;

    BucketNode **buckets = calloc(sizeof(BucketNode), num_buckets);
    newHashMap->buckets = buckets;
    return newHashMap;
}

// @brief Construct a new HashMap of the given size, and re-hash all
//        the values from the old one. This needs to be done when expanding
//        or shrinking the Dynamic HashMap during insertion and deletion.
//
// @param hm         The old HashMap
// @param new_size   Required size of new HashMap
//
// @return           New HashMap (old one must be freed).
//
// @TODO: Implement this function. For the sake of consistency, the automarker
//        will expect you to re-hash all the elements in a specific order. Go
//        through the buckets sequentially from [0 - hm->num_buckets], and for
//        each one insert the nodes in the linked list sequentially. See the
//        test casesfor example behaviour.
HashMap *HashMap_Resize(HashMap *hm, int new_size) {
    HashMap *newhm = newHashMap(new_size, hm->func);

    for (int i = 0; i < hm->num_buckets; i++) {
        BucketNode *node = hm->buckets[i];
        while (node) {
            HashMap_Add(newhm, node->key, node->value);
            node = node->next;
        }
    }
    HashMap_Free(hm);
    return newhm;
}

// @brief Add a key-value pair to the HashMap. Dynamically resize
//        the hashmap when at capacity.
//
// @param hm     HashMap
// @param key    Key to be inserted
// @param value  Corresponding Value
//
// @return     Pointer to resulting HashMap (useful when you expand)
//
// @TODO: Implement this function. Here are some notes in implementation:
//        (1) If the key exists, replace the value.
//
//         (2) If the key doesn't exist, add the new BucketNode at the
//            *head* of the corresponding linked list
//
//        (3) To get the array into the buckets[] array, use the hash
//            function inside `hm` and then take that value mod the
//            number of buckets:
//                      idx = hash(key) % num_buckets
//
//        (4) AFTER you have inserted the new element, if the number
//            of elements in the HashMap is >= the number of buckets,
//            double the size of the HashMap and re-hash all the elements.
HashMap *HashMap_Add(HashMap *hm, const char *key, const char *value) {
    //index
    int idx = hm->func(key) % hm->num_buckets;
    //search for item
    int found = 0;
    BucketNode *node = hm->buckets[idx];
    while (node && !found) {
        if (strcmp(node->key, key) == 0) {  // found it
            strcpy(node->value, value);
            found = 1;
        }
        node = node->next;
    }

    //insert if not found
    if (!found) {
        BucketNode *headNode = hm->buckets[idx];

        BucketNode *newHead = calloc(sizeof(BucketNode), 1);
        strcpy(newHead->key, key);
        strcpy(newHead->value, value);
        newHead->next = headNode;
        hm->buckets[idx] = newHead;
    }

    hm->num_elems++;  // increment num elements

    return hm->num_elems >= hm->num_buckets ? HashMap_Resize(hm, hm->num_buckets * 2) : hm;
}

// @brief Find the value of the given key in the HashMap
//        Return NULL if key does not exist.
//
// @param hm   HashMap
// @param key  Key to be queried in the hashmap
//
// @return     The corresponding value to the key, or NULL.
//
// @TODO: Implement this function
char *HashMap_Find(HashMap *hm, const char *key) {
    BucketNode *node = hm->buckets[hm->func(key) % hm->num_buckets];

    while (node) {
        if (strcmp(node->key, key) == 0) {
            return node->value;
        }
        node = node->next;
    }
    return NULL;
}

// @brief Delete a key-value pair from the HashMap. Dynamically resize
//        the HashMap if necessary.
//
// @param hm   HashMap
// @param key  Key for which the pair needs to be deleted.
//
// @return     Pointer to resulting HashMap (useful when you shrink)
//
// @TODO: Implement this function. Here are some notes in implementation:
//        (1) If the key doesn't exist, don't do anything.
//
//         (2) Don't reorder the rest of the list when removing the node
//
//         (3) AFTER deleting the element, if num_elems < num_buckets/4, then
//             shrink the HashMap by half. (Similar to Dynamic Arrays). You'll
//             need to re-hash all the elements.
HashMap *HashMap_Delete(HashMap *hm, const char *key) {
    BucketNode *node = hm->buckets[hm->func(key) % hm->num_buckets];
    BucketNode *trailingNode = NULL;
    while (node) {
        if (strcmp(node->key, key) == 0) {  // found
            if (trailingNode) {
                trailingNode->next = node->next;
            } else {
                hm->buckets[hm->func(key) % hm->num_buckets] = node->next;
            }
            free(node);
            break;
        }
        trailingNode = node;
        node = node->next;
    }
    hm->num_elems--;  // decrement num elements
    return hm->num_elems < hm->num_buckets / 4 ? HashMap_Resize(hm, hm->num_buckets / 2) : hm;
}

// @brief Frees all the memory used by the HashMap
//
// @param hm   HashMap
//
// @TODO: Implement this function. You will need to use valgrind to properly
//        check the functionality.
void HashMap_Free(HashMap *hm) {
    for (int i = 0; i < hm->num_buckets; i++) {
        free(hm->buckets[i]);
    }
    free(hm->buckets);
    free(hm);
    return;
}

//util function to print out easy to read hashmap
void printHashmap(HashMap *hm) {
    printf("\n");
    for (int i = 0; i < hm->num_buckets; i++) {
        printf("[ %d ]", i);
        BucketNode *node = hm->buckets[i];

        while (node) {
            printf("--->{%s = %s}", node->key, node->value);
            node = node->next;
        }
        printf("\n");
    }
    printf("\n");
}