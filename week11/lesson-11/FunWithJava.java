import java.util.ArrayList;

// Everything is a class. The class name is the filename (they have to be exactly the same).
public class FunWithJava {

    // Just like C and C++, the program starts with 'main'
    public static void main(String[] args) {

        // Java is a typed language and so we have to define
        // the data type of all our variables.
        int value = 150;

        // An array is a list. To tell the compiler that we want to
        // reserve memory (i.e., 'instantiate') we use the "new" keyword.
        // Now the variable 'list' is an object that references where
        // in memory the list (or array) is located. Technically, unlike
        // C++, the Java Virtual Machine (JVM) knows the location and
        // our program does not.
        int[] list = new int[5];

        // To add to a primitive array, we have to reference the array indexes:
        list[0] = 0;
        list[1] = 1;
        list[2] = 2;

        // Unlike Python, there are no functions available to use with our array,
        // so we can't do stuff like list.append. If we want that kind of
        // functionality then we have to create an ArrayList. The '<Integer>'
        // part tells the compiler what type of object the list will hold.
        ArrayList<Integer> myArrayList = new ArrayList<>();

        // Now we can add to the list
        myArrayList.add(1);
        myArrayList.add(2);
        myArrayList.add(3);

        // We can create our own classes (either in another file or within another
        // class)
        class MyClass {

            // These are the class variables. In python, we use self.<name> inside of the
            // __init__ function to create class variables, in Java we place them outside
            // of any function/method. And of course, we have to declare their types:
            int x;
            int y;
            ArrayList<Integer> list;

            // The constructor is called when a class is instantiated (e.g., new MyClass() )
            public MyClass(int x, int y, ArrayList<Integer> list) {
                this.x = x;
                this.y = y;
                this.list = list;
            }
        }

        // Outside of the MyClass, but inside of FunWithJava class, we can instantiate
        // MyClass and pass in the appropriate parameters that the constructor takes.
        // The type of data passed in has to match the type of data received (meaning
        // that if you pass in an int, then the matching parameter in the
        // constructor has to be declared as an int)
        MyClass myClass = new MyClass(list[0], value, myArrayList);

        System.out.println(myClass.x);
        System.out.println(myClass.y);
        System.out.println(myClass.list);
    }
}
