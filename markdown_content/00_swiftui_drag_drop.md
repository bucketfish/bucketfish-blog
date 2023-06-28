^title the simplest guide to onDrag and onDrop in SwiftUI
^category technicality
^readingtime 4
^description just implementing a very simple onDrag and onDrop in SwiftUI. that is all. no hassle.
^date 27 june 2023
^slug swiftui-drag-drop

this post was done using xcode 14.3, in swift 5. [jump to completed code!](#completed-code)

when i first tried implementing drag and drop into my project, all i could find was lots of long, extensive tutorials — which is super helpful for learning about the uses of the features, but i had to carefully strip what i needed down, and i struggled a lot with figuring out what did what. so here is the fastest, simplest guide to implementing onDrag and onDrop in SwiftUI.

before we begin: a quick overview of onDrag and onDrop. these features tie into the greater ecosystem of dragging and dropping data between all kinds of apps. the data sent has to conform to a [uniform type identifier](https://developer.apple.com/documentation/uniformtypeidentifiers/uttype), which basically enforce the kind of data that your view can send or receive.

for example, a view that receives `public.text` (often used to transfer plain strings) can receive it from anywhere, much like copy-pasting! keep this in mind when creating your app: a small prototype might not need to take this into consideration, but handling unwanted input is something essential in the long run.

alright, let's dive in to a small, quick, speedy sample.

---

## the important bit

we begin with a quick new project — boilerplate SwiftUI code for a blank view. let's also create two `Text()` views with lots of padding and an overlay rectangle, so we can see where they are — these will be our drag and drop locations!

~~~~swift
import SwiftUI

struct ContentView: View {
  var body: some View {
    // drop box
    Text("nothing here!")
      .padding(30)
      .overlay(
        Rectangle()
        .stroke(.white)
        )

    // drag box
    Text("data to transfer")
      .padding(30)
      .overlay(
        Rectangle()
        .stroke(.white)
        )
  }
}
~~~~

we need some way to keep track of the data that's being displayed. it's easy to create a State variable for that, which will refresh the view every time it's changed. we'll just quickly change two lines.

~~~~swift hl_lines="3 9"
struct ContentView: View {
  @State var textToDisplay = "nothing here!"
  var body: some View {
    // drop box
    Text(textToDisplay)
      .padding(30)
~~~~

![preview of how it looks like so far](../../assets/00/0.png)

and now for the meat of it. let's start with the drag first — that's the easiest.

1. we need to add an onDrag modifier to the view so that swift knows that this view is draggable
2. we need to specify what kind of data should be transferred in the drag
3. optionally, we can also provide a custom _preview_ to the dragged view, which will show up and follow the cursor when it's dragged.

we'll just get our drag box to send a string, "some text!", to the other one. to do this, the `NSItemProvider` comes in handy as a class to quickly create an `NSItem`, which is what you need to send data through drag and drop.

~~~~swift hl_lines="7 8 9 10 11 12"
// drag box
Text("some text!")
  .padding(30)
  ...
  .onDrag {
    NSItemProvider(object: String("some text!") as NSString)
  }    
~~~~

now try dragging it!

you'll find that it seems to only work occasionally. look closer, and it actually only drags when your cursor is clicking on the text and not anywhere else in the box — this is way too precise for our needs. luckily, there's an easy fix: we simply need to add a `contentShape` modifier in order to click anywhere to drag it.

~~~~swift hl_lines="5 13"
Text(textToDisplay)
  .padding(30)
  .contentShape(Rectangle())

Text("some text!")
   .padding(30)
   .contentShape(Rectangle())
   .onDrag { ... }
~~~~

![preview of dragging](../../assets/00/1.gif)

awesome. all we have to do now is to implement dropping — this comes in a few steps, too.
1. add an onDrop modifier to the view, and specify what content can be received — in this case, we only want  `public.text`
2. make sure that we have at least one item in the dropped stuffs and pick it out
3. load the item's content as a `public.text`
4. make sure that the content can be interpreted as binary data
5. decode the data to get our string!
6. tell swift that the drop operation completed successfully

and here it is, in code.

~~~~swift
// 1. onDrop modifier
.onDrop(of: ["public.text"], isTargeted: nil, perform: { itemProvider, _ in
  // 2. make sure we have at least one item
  if let item = itemProvider.first {
    // 3. load item as public.text
    item.loadItem(forTypeIdentifier: "public.text", options: nil) { (data, err) in

      // 4. make sure that it can be interpreted as binary data
      if let text = data as? Data{

        // 5. decode string and assign it to display
        textToDisplay = String(decoding: text, as: UTF8.self)

        }
      }
    }
    // 6. drop operation completed successfully!
    return true
  })
~~~~
![final demonstration of completed drag and drop](../../assets/00/2.gif)

and there we go! simplest possible implementation of onDrag and onDrop. if you're interested in more detailed usages, here are some more advanced tutorials on  <a href="https://www.kodeco.com/21679742-drag-and-drop-tutorial-for-swiftui" target="_blank">kodeco.com</a> and <a href="https://swiftui-lab.com/drag-drop-with-swiftui/" target="_blank">swiftui-lab.com</a>. happy dragging!

---

## <a name="completed-code"></a>completed code

~~~~swift
import SwiftUI

struct ContentView: View {
  @State var textToDisplay = "nothing here!"

  var body: some View {
    Text(textToDisplay)
      .padding(30)
      .contentShape(Rectangle())
      .overlay(Rectangle().stroke(.white))
      .onDrop(of: ["public.text"], isTargeted: nil, perform: { itemProvider, _ in
        if let item = itemProvider.first {
          item.loadItem(forTypeIdentifier: "public.text", options: nil) { (data, err) in
            if let text = data as? Data{
              textToDisplay = String(decoding: text, as: UTF8.self)
            }
          }
        }
        return true
      })

    Text("data to transfer")
      .padding(30)
      .contentShape(Rectangle())
      .overlay(Rectangle().stroke(.white))
      .onDrag { NSItemProvider(object: String("some text!") as NSString) }    
  }
}
~~~~
