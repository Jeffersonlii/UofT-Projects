/**
 *                        Min-Heaps
 * 
 * This is the A2 section of your coding assignment. You will only submit this
 * along with the A3 section when A3 is due, but it is recommended that you
 * complete this early on so you have time to work on second part of this
 * assignment (in `marcher.c` ).
 * 
 * Please make sure you read the blurb in `minheap.h` to ensure you understand 
 * how we are implementing min-heaps here and what assumptions / requirements 
 * are being made.
 * 
 * CSCB63 Winter 2021 - Assignment 2/3
 * (c) Mustafa Quraish
 */

#include "minheap.h"

/**
 * Allocate a new min heap of the given size.
 * 
 * TODO: 
 *  Allocate memory for the `MinHeap` object, and the 2 arrays inside it.
 *  `numItems` should initially be set to 0, and all the indices should be
 *   set to -1 to start with (since we don't have anything in the heap).
 */
MinHeap *newMinHeap(int size)
{

  MinHeap *newMinHeap = calloc(sizeof(MinHeap), 1);
  newMinHeap->maxSize = size;
  newMinHeap->numItems = 0;

  newMinHeap->arr = calloc(size, sizeof(HeapElement));
  newMinHeap->indices = calloc(size, sizeof(HeapElement));

  for (int i = 0; i < size; i++)
  {
    newMinHeap->indices[i] = -1;
  }

  return newMinHeap; // Allocate and return heap.
}

/**
 * Swaps elements at indices `a` and `b` in the heap, and also updates their
 * indices. Assumes that `a` and `b` are valid.
 * 
 * NOTE: This is already implemented for you, no need to change anything.
 */
void swap(MinHeap *heap, int a, int b)
{
  // Swap the elements
  HeapElement temp = heap->arr[a];
  heap->arr[a] = heap->arr[b];
  heap->arr[b] = temp;

  // Refresh their indices
  heap->indices[heap->arr[a].val] = a;
  heap->indices[heap->arr[b].val] = b;
}

/**
 * Add a value with the given priority into the heap.
 * 
 * TODO: Complete this function, and make sure all the relevant data is updated
 *      correctly, including the `indices` array if you move elements around. 
 *      Make sure the heap property is not violated. 
 * 
 * You may assume the value does not already exist in the heap, and there is
 * enough space in the heap for it.
 */
void heapPush(MinHeap *heap, int val, double priority)
{

  HeapElement newHeapElement;
  newHeapElement.priority = priority;
  newHeapElement.val = val;

  int i = heap->numItems;

  heap->arr[i] = newHeapElement; // push to end of heap array
  heap->indices[val] = i;        // add the indice

  //percolate up
  int parentIndex;
  while (heap->arr[parentIndex = floor((i + 1) / 2) - 1 < 0
                                     ? 0
                                     : floor((i + 1) / 2) - 1]
             .priority > priority)
  { //while parent is higher prior than self
    swap(heap, parentIndex, i);
    i = parentIndex; //update self index to the parent we just swapped to
  }
  heap->numItems++;
  return;
}

/**
 * Extract and return the value from the heap with the minimum priority. Store
 *  the priority for this value in `*priority`. 
 * 
 * For example, if `10` was the value with the lowest priority of `1.0`, then
 *  you would have something that is equivalent to:
 *      
 *        *priority = 1.0;
 *        return 10;
 * 
 * TODO: Complete this function, and make sure all the relevant data is updated
 *      correctly, including the `indices` array if you move elements around. 
 *      Make sure the heap property is not violated. 
 * 
 * You may assume there is at least 1 value in the heap.
 */
int heapExtractMin(MinHeap *heap, double *priority)
{
  // printf("\n start \n");

  //min is at the front of the array
  double minPrio = heap->arr[0].priority;
  int minVal = heap->arr[0].val;

  //setup index for swap
  heap->indices[minVal] = -1;

  //swap min with max
  swap(heap, heap->numItems - 1, 0);
  heap->numItems--; // remove the last element from heap

  //heapify

  int leftIndex, rightIndex, i = 0;
  while (((leftIndex = (i + 1) * 2 - 1 < heap->numItems ? (i + 1) * 2 - 1 : -1) != -1) |
         ((rightIndex = (i + 1) * 2 < heap->numItems ? (i + 1) * 2 : -1) != -1))
  {
    int swappingIndex;

    if (leftIndex == -1)
    {
      swappingIndex = rightIndex;
    }
    else if (rightIndex == -1)
    {
      swappingIndex = leftIndex;
    }
    else
    {
      swappingIndex = heap->arr[leftIndex].priority < heap->arr[rightIndex].priority ? leftIndex : rightIndex;
    }
    if (heap->arr[swappingIndex].priority > heap->arr[i].priority)
      break;
    swap(heap, swappingIndex, i);
    i = swappingIndex;
  }

  // printf("\n %f, %i \n\n", minPrio, minVal);

  *priority = minPrio; // Set correct priority
  return minVal;       // Return correct value
}

/**
 * Decrease the priority of the given value (already in the heap) with the
 * new priority.
 * 
 * NOTE: You will find it helpful here to first get the index of the value
 *       in the heap from the `indices` array.
 * 
 * TODO: Complete this function, and make sure all the relevant data is updated
 *      correctly, including the `indices` array if you move elements around. 
 *      Make sure the heap property is not violated. 
 * 
 * You may assume the value is already in the heap, and the new priority is
 *  smaller than the old one (caller is responsible for ensuring this).
 */
void heapDecreasePriority(MinHeap *heap, int val, double priority)
{
  int i = heap->indices[val];
  heap->arr[i].priority = priority; // reassign new prio

  //percolate
  int parentIndex;
  while (heap->arr[parentIndex = floor((i + 1) / 2) - 1 < 0
                                     ? 0
                                     : floor((i + 1) / 2) - 1]
             .priority > priority)
  { //while parent is higher prior than self
    swap(heap, parentIndex, i);
    i = parentIndex; //update self index to the parent we just swapped to
  }
  return; // Decrease priority before return
}

/**
 * Free the data for the heap. This won't be marked, but it is always good
 * practice to free up after yourself when using a language like C.
 */
void freeHeap(MinHeap *heap)
{
  free(heap->arr);
  free(heap->indices);
  free(heap);

  return; // Free heap and it's arrays
}
