This template shows off a simple CRUD App, which allows you to create,
read, update, and delete menu items.

## Components

The example is composed of three main components:

1. ItemList: Displays the list of menu items and allows the user to add new
   items, delete existing items, or select an item for editing.
2. ItemEditor: Allows the user to edit the details of a selected menu item or
   create a new item.
3. CrudPage: Combines the ItemList and ItemEditor component and add some logic.

## Outcome

In this example you will learn how to populate your application with your own
data, add new items, edit existing items, and delete items. The data is stored
in the `menu_item_set` state of the `CrudPage` component.
In addition, you will learn how to pass data between components and how to
trigger actions in one component from another using rio's EventHandler.
