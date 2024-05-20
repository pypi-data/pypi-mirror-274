# ERAS
Easily Run AI Shell allows you to run shell commands using natural language.   

No more having to leave the terminal to look up how to run a command!

# Demo
[Eras Demo](https://youtu.be/T7KRDwi5HDo)

[![Video Thumbnail](https://img.youtube.com/vi/T7KRDwi5HDo/0.jpg)](https://youtu.be/T7KRDwi5HDo)


<video src="./eras-demo.mov" controls></video>

# Install
```
% pip install eras
```

If you get an error about externally-managed-environment it's because you have python installed via homebrew, and need to use pipx instead:

pipx
``` 
brew install pipx
pipx ensurepath
pipx install eras\
```
With pipx you may need to open a new terminal window or source .zshrc a couple of times.

# Use
The first use of Eras will prompt you to enter an OpenAI key, which it will save to your profile as `ERAS_OPENAI_KEY`

The first use will also prompt you to allow accessibility features for Terminal.app, which is required to allow Eras to populate
the terminal with the shell command.

![img.png](https://i.imgur.com/y3OLDuG.png)


When you ask Eras a question, it will use AI to create a shell command, then populate your next terminal line with the command, so all you have to do is review and press enter.

## Examples
```
% eras list files
% ls
...
% eras create a new file named jason.txt with contents "hello world"
% echo "hello world" > jason.txt
...

```


