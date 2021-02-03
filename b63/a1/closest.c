/************************************************************************
 *                       CSCB63 Winter 2021
 *                  Assignment 1 - AVL Trees
 *                  (c) Mustafa Quraish, Jan. 2021
 *
 * This is the file which should be completed and submitted by you
 * for the assignment. Make sure you have read all the comments
 * and understood what exactly you are supposed to do before you
 * begin. A few test cases are provided in `testClosest.c`, which
 * can be run on the command line as follows:
 *
 *  $> gcc testClosest.c -o testClosest
 *  $> ./testClosest [optional testname]  (or .\testClosest.exe if on Windows)
 *
 * I strongly advise that you write more test cases yourself to see
 * if you have expected behaviour, especially on the edge cases for
 * insert(). You are free to make any reasonable design choices for
 * the implementation of the data structure as long as (1) the outputs
 * are consistent with the expected results, and (2) you meet the
 * complexity requirement. Your closestPair() function will only
 * be tested with cases where there are unique solutions.
 *
 * Mark Breakdown (out of 10):
 *  - 0 marks if the code does not pass at least 1 test case.
 *  - If the code passes at least one test case, then:
 *    - Up to 6 marks for successfully passing all the test cases
 *    - Up to 4 marks for meeting the complexity requirements for 
 *        the functions as described in the comments below.
 *
 ************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#define LEFT 1
#define RIGHT -1



/**
 * This defines the struct(ure) used to define the nodes
 * for the Reb-Black tree we are going to use for this
 * assignment. You need to add some more fields here to be
 * able to complete the functions in order to meet the
 * complexity requirements
 */
typedef struct avl_node {
  // Stores the value (key) of this node
  int value;

  // Pointers to the children
  struct avl_node *left;
  struct avl_node *right;

  // TODO: Add the other fields you need here to complete the assignment!
  //      (Hint: You need at least 1 more field to keep balance)
  int height;

  struct avl_node *closest_a;
  struct avl_node *closest_b;

  struct avl_node *smallest_node;
  struct avl_node *biggest_node;

} AVLNode;;

/**
 * This function allocates memory for a new node, and initializes it. 
 * The allocation is already completed for you, in case you haven't used C 
 * before. For future assignments this will be up to you!
 * 
 * TODO: Initialize the new fields you have added
 */
AVLNode *newNode(int value) {
  AVLNode *node = calloc(sizeof(AVLNode),1);
  if (node == NULL) {  // In case there's an error
    return NULL;
  }

  node->value = value;
  node->left = NULL;
  node->right = NULL;

  // Initialize values of the new fields here...
  node->height = 1;

  node->closest_a = NULL;
  node->closest_b = NULL;

  node->smallest_node = node;
  node->biggest_node = node;
  return node;
}

int max(x,y){
  return x > y ? x : y;
}
int min(x,y){
    return x < y ? x : y;
}
int abs(x){
    return x < 0 ? -1*x : x;
}
AVLNode *setClosests(AVLNode *root){ 
  if(root->left == NULL && root->right == NULL){
    root->closest_a = NULL;
    root->closest_b = NULL;
    root->smallest_node = root;
    root->biggest_node = root;
    return root;//if no children, reset to leaf node 
  }

  int left_min = 1000001;
  int right_min = 1000001;
  int left_gap = 1000001;
  int right_gap = 1000001;

  if(root->left != NULL){ 
    root->smallest_node = root->left->smallest_node;// set smallest to left edge 

    left_gap = root->value - root->left->biggest_node->value;//left gap is (self - max of left)
    if(root->left->closest_a != NULL){

      left_min = root->left->closest_b->value - root->left->closest_a->value; //get left min if exists
    }
  }
  if (root->right != NULL){
    root->biggest_node = root->right->biggest_node;//set biggest to right edge 

    right_gap = root->right->smallest_node->value - root->value;//right gap is (min of right - self)
    if(root->right->closest_a != NULL){
        right_min = root->right->closest_b->value - root->right->closest_a->value;//get right min if exists
    }
  }

  int abs_min = min(left_min, min(right_min, min(left_gap, right_gap)));
  if(left_min == abs_min){
    root->closest_a = root->left->closest_a;
    root->closest_b = root->left->closest_b;
  }else if (right_min == abs_min){
    root->closest_a = root->right->closest_a;
    root->closest_b = root->right->closest_b;
  }else if (left_gap == abs_min){
    root->closest_a = root->left->biggest_node;
    root->closest_b = root;
  }else{ //right_gap == abs_min
    root->closest_a = root;
    root->closest_b = root->right->smallest_node;
  }

  return root;
}
AVLNode *rotate(AVLNode *root,int direction){ 
  AVLNode *new_root;
  AVLNode *straggler;
  if(direction == LEFT){
    straggler = root->right->left;

    new_root = root->right;
    new_root->left = root;
    root->right = straggler;
    
  }else{//direction == RIGHT
    straggler = root->left->right;

    new_root = root->left;
    new_root->right = root;
    root->left = straggler;
  }
  int left_height = root->left == NULL ? 0 : root->left->height;
  int right_height = root->right == NULL ? 0 : root->right->height;
  root->height = max(left_height,right_height) + 1; //recalculate height

  left_height = new_root->left == NULL ? 0 : new_root->left->height;
  right_height = new_root->right == NULL ? 0 : new_root->right->height;
  new_root->height = max(left_height,right_height) + 1; //recalculate height

  root = setClosests(root);
  new_root = setClosests(new_root);

  return new_root;

}

/**
 * This function is supposed to insert a new node with the give value into the 
 * tree rooted at `root` (a valid AVL tree, or NULL)
 *
 *  NOTE: `value` is a positive integer in the range 1 - 1,000,000 (inclusive)
 *       The upper bound here only exists to potentially help make the 
 *                implementation of edge cases easier.
 *
 *  TODO:
 *  - Make a node with the value and insert it into the tree
 *  - Make sure the tree is balanced (AVL property is satisfied)
 *  - Return the *head* of the new tree (A balance might change this!)
 *  - Make sure the function runs in O(log(n)) time (n = number of nodes)
 * 
 * If the value is already in the tree, do nothing and just return the root. 
 * You do not need to print an error message.
 *
 * ----
 * 
 * An example call to this function is given below. Note how the
 * caller is responsible for updating the root of the tree:
 *
 *  AVLNod *root = (... some tree is initialized ...);
 *  root = insert(root, 5); // Update the root!
 */
AVLNode *insert(AVLNode *root, int value) {

  if(root == NULL) {//base case
    return newNode(value);
  } 

  //1 => go left, -1 => go right, 0 => already exists
  int direction = root->value > value ? LEFT : root->value < value ? RIGHT : 0;

  if(direction == LEFT){//go left
    root->left = insert(root->left, value);
  }
  else if(direction == RIGHT){//go right
    root->right = insert(root->right, value);
  }
  else{
    return root; //do nothing if node exists
  }

  int left_height = root->left == NULL ? 0 : root->left->height;
  int right_height = root->right == NULL ? 0 : root->right->height;
  root->height = max(left_height,right_height) + 1; //recalculate height

  root = setClosests(root);

  int balance_factor =  left_height - right_height;
  if(abs(balance_factor) > 1){ //need to rotate
    int heavy_side = balance_factor > 1 ? LEFT : RIGHT;

    if(heavy_side == LEFT && root->left->value < value) { // left to right bend, double rotate
      root->left = rotate(root->left, LEFT);
    }
    else if (heavy_side == RIGHT && root->right->value > value){ // right to left bend, double rotate
      root->right = rotate(root->right, RIGHT);
    }
    return rotate(root, direction == LEFT ? RIGHT : LEFT ); // rotate opposite to heavy side
  }
 
  return root;
}

/**
 * This function returns the closest pair of points in the tree rooted
 * at `root`. You can assume there are at least 2 values already in the
 * tree. Since you cannot return multiple values in C, for this function
 * we will be using pointers to return the pair. In particular, you need
 * to set the values for the two closest points in the locations pointed
 * to by `a` and `b`. For example, if the closest pair of points is
 * `10` and `11`, your code should have something like this:
 *
 *   (*a) = 10 // This sets the value at the address `a` to 10
 *   (*b) = 11 // This sets the value at the address `b` to 11
 *
 * NOTE: Make sure `(*a)` stores the smaller of the two values, and
 *                 `(*b)` stores the greater of the two values.
 * 
 * NOTE: The test cases will have a unique solution, don't worry about 
 *        multiple closest pairs here.
 *
 *
 * TODO: Complete this function to return the correct closest pair.
 *       Your function should not be any slower than O(log(n)), but if 
 *       you are smart about it you can do it in constant time.
 */
void closestPair(AVLNode *root, int *a, int *b) {

  (*a) = root->closest_a->value;
  (*b) = root->closest_b->value; 
  return;
}

/******************************************************************************
 * QUERY() and DELETE() are not part for this assignment, but I recommend you
 * try to implement them on your own time to make sure you understand how AVL
 * trees work.
 *
 *                              End of Assignment 1
 *****************************************************************************/
