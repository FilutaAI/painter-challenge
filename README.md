# Problem Description
## The Input
- Given is a connected planar graph with $n$ vertices and $m$ edges.
- One of the vertices is labeled as the *start node*
- Some of the vertices are labeled as *source nodes*.

## The Goal 
The goal is to generate a plan (a sequence of actions) for a painter agent that can travel on the graph along the edges and paint the vertices.

## The Rules
- There are four colors available
- Adjacent vertices (connected by an edge) must be painted with different colors
- The painter agent can carry at most two buckets of paint
- The painter agent starts on the *start node* and he is not carrying any buckets. In each step they can perform one of the following three kinds of actions
  - color the vertex where the painter is located with a certain color. The painter must carry a bucket with that color and it will be consumed after the action.
  - move to an adjacent vertex that is not yet painted (a vertex that has been once painted cannot be entered anymore)
  - collect a bucket with a certain color of paint. The painter has to be located on vertex labeled as *source node*

## Example
