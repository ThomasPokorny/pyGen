``` 
 ________  ___    ___ ________  _______   ________      
|\   __  \|\  \  /  /|\   ____\|\  ___ \ |\   ___  \    
\ \  \|\  \ \  \/  / | \  \___|\ \   __/|\ \  \\ \  \   
 \ \   ____\ \    / / \ \  \  __\ \  \_|/_\ \  \\ \  \  
  \ \  \___|\/  /  /   \ \  \|\  \ \  \_|\ \ \  \\ \  \ 
   \ \__\ __/  / /      \ \_______\ \_______\ \__\\ \__\
    \|__||\___/ /        \|_______|\|_______|\|__| \|__|
         \|___|/                                        
                                                   

```
# pyGen 
A lightweight Java Class generation Tool

Calling Synopsis
```
python pyGen.py gen.json

python pyGen.py  [json-file]

```
# Examples

When called with the following .json File

```json
{
    "Transport" : 
        {   "abstract":true,
            "fields": [ {"name":"generatedBool", "t":"boolean", "gs":true},  {"name":"engine", "t":"Engine"},  {"name":"someMap", "t":"Map<String,Integer>"}   ] ,
            "methods":[ {"name":"someGeneratedTestMethod", "return":"Long", "param":"ArrayList<Integer> ints, boolean isTrue"} ,
                        {"name":"someAbstractTestMethod", "abstract":true, "return":"Long", "param":"ArrayList<Integer> ints, boolean isTrue"} 
                        ] 
        },
 "Engine" : 
        {   "interface":true, 
            "methods":[ {"name":"range", "return":"int"} ]
        },

}
```

The resulting Java Files look like this:

(Transport.java)
```java
public abstract class Transport
{

	private boolean generatedBool;

	private Engine engine;

	private Map<String,Integer> someMap;

	public Long someGeneratedTestMethod(ArrayList<Integer> ints, boolean isTrue)
	{
	}

	public abstract Long someAbstractTestMethod(ArrayList<Integer> ints, boolean isTrue);

	public boolean getGeneratedbool(){
		return generatedBool;
	}

	public void setGeneratedbool(boolean generatedBool){
		this.generatedBool = generatedBool;
	}
}
```

and 

(Engine.java)
```java
public interface Engine
{

	public int range();
}
```
(Note that import -, package - and method return statements are not generated yet!)
