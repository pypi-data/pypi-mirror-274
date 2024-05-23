# Cell References (more stuff in progress)

## Implementation

We want to update the code to show the "filled-in" stuff so each reference should be fully-specified by the time we publish the code back. This means finding unscoped identifiers, and taking any scoped identifiers and updating as necessary...

The whole is_external_link thing is interesting because we want to know that another cell defines the variable and we can reference it. In effect, we want the most recently defined variable that isn't the current cell. Or... we have some semantics to duplicate the cell so we can string this along as was indicated.

Currently, _add_links is run when the output tags are passed down. This is fine, but it means the last **defined** cell is the one that sits in __links__ instead of the last **exectued** cell.

We have an issue where cell_id is updated by the ^ but somehow isn't persisted?

## Versioning

We may also want a variable to reference a cell but **not update** each time the cell changes. (This is probably not the best idea... use the cell magic qualifier for the cell that shouldn't automatically activate downstream reactivity.) This isn't the best but may be useful when a cell has a long-running computation. Here, we can break the reactive chain by adding the exclamation mark qualifier (`!`) to the reference. Thus, the code `df$!43de1f` will use the last-computed output `df` from cell `43de1f`, regardless of whether the cell's code has changed.

How do we deal with the whole downstream updating? We can use the qualifier on the last line `$$ df` to indicate that it should always be updated or some magic at the top? Magic at the top seems more consistent? Problem is that we then have conflicts between the references and the cells themselves (the ! modifier)


If we assume that each cell has associated versions, we can also have version-associated ways to reference variables. Thus, if we load dataset `data-2022.csv` as `df` and then run some operations on it, we might have

```
[ab3]: df = pd.load_csv('data-2022.csv')

[4e3]: df = df$ab3.astype{'sales': 'float32'}

[e43]: df$4e3.sales.mean()
```

Then, we go back and change the first cell (`ab3`) to now load `'data-2023.csv'`. We can create a new "branch" for this analysis and give it a name (`analyze2023`) but it also has a version id (`b23ffe`); call the first version `11e435`. If we rerun the three cells above (with the change to `ab3`), we now have two parallel paths of computation but these are versioned. Effectively, we have references that can be scoped to the different versions. Specifically, we have `df$11e435:ab3` referenced in cell `a32fb1:4e3` in the first path, and a `df$b23ffe:ab3` referenced in cell `79b4e1:4e3`. These can be referenced directly, but note that this may get confusing quickly...

We need that any unversioned reference always references the most recent version of the cell in the current branch (the state at the head of the branch). However, we may want to do some comparative analysis between 2022 and 2023. To do this, we need to reference the results from `4a3` from the different versions. We can write this directly, but note that this is a bit weird because we may not be able to see the cells that generate these results. If we allow a user to make a **result** sticky, then they will always see this result, regardless of the code that generated it. Then, the user can alias the result accordingly (`results2022`) and write code to reference this variable directly. If they want to go back and edit the cells that generate this result, they can, and this will effectively create a new branch to capture the change. In other words, we create copies of these cells that can be edited inline.

This is the concept of aliases where a name stands in for a persistent, versioned reference. It probably makes sense for a user to be able to reference a particular output with an alias as well as by defining a variable name. Note that we have to be careful about using that alias as a variable, however. Maybe we can allow the local variable name to shadow and only worry when we have an output with the same name as an alias?

Really, what we want is the ability to scroll through a gallery of outputs associated with a cell and not worry about how that output was generated until we need to edit something. When a cell is referenced, we show it and its dependencies. When those cells are duplicates of existing cells, these become a grouping that makes clear that the block is separate (and dated). When the cell is no longer referenced, those blocks disappear.