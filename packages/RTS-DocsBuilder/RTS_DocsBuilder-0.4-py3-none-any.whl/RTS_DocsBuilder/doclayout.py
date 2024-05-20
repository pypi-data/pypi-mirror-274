from RTS_WebUIBuilder.RDocument import RDocument
from RTS_WebUIBuilder.RBox import RBox
from RTS_WebUIBuilder.RLabel import RLabel
from RTS_WebUIBuilder.RTitle import RTitle
from RTS_WebUIBuilder.RGroupStyle import RGroupStyle
from RTS_WebUIBuilder.RAdditions import rgba, rgb
from RTS_WebUIBuilder.RInput import RTextInput
from RTS_WebUIBuilder.RQuickScripts import RQuickScripts
import random, string, inspect, os, importlib



import re
class DocLayout:
    

    def __init__(self,*, path:str, static:bool=False):

        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame[0])
        module_file_path = caller_module.__file__
        module_file_path = os.path.dirname(module_file_path)

        path_parts = module_file_path.split('docs')


        self._modulename = os.path.basename(os.path.dirname(path_parts[0]))
        
        whereami = os.path.normpath(path_parts[1]).split(os.sep)[1:3]  # Limit to 2 segments
        
        if len(whereami) == 1:
            whereami.append(None)
        
        self._currentTopic , self._currentsub = whereami
        self._currentTopic = re.sub(r'^[a-z]--', '', self._currentTopic)
        if self._currentsub:
            self._currentsub = re.sub(r'^[a-z]--', '', self._currentsub)
        print("--------------------------------------------------------------------")
        print(self._modulename + " > " + self._currentTopic + " > " + str(self._currentsub))
        
        module_name = self._modulename + ".docs.loads"
        module = importlib.import_module(module_name)

        docMemory = module.docMemory
        #print("rlos",docMemory.initDocs.topics, docMemory.initDocs.subtopics)
        

        if not isinstance(path, str):
            raise ValueError("path must be a string.")
        if not isinstance(static, bool):
            raise ValueError("static must be a boolean.")
        if not path:
            raise ValueError("path cannot be empty.")
        dom = RDocument(documentRoute=path, static=False)
        dom.body.style.margin()
        dom.body.style.padding()
        #dom.body.style.draw(width="100%", height="102px")
        dom.importFonts(font="Roboto", fontURL="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap")
        

       
        dom.body.removeScrollbar()
        dom.defaultFont("Roboto")
        dom.body.style.colorize(background=rgba(0,0,0,0.3))
        dom.body.style.overflow(X="hidden", Y="hidden")
        redir = RQuickScripts()
        redir.redirectFunction()
        dom.body.redirect = redir

        #
        # topbox layout
        #
        topbox = RBox()
        self.topbox = topbox
        topbox.style.margin()
        topbox.style.draw(width="100%", height=100,moveX=-2)
        topbox.style.colorize(background=rgb(255,255,255))
        topbox.style.border(style="solid", width=1, color="#000000")
        topbox.style.roundCorners(bottomright=20)
        
        searchbar = RTextInput()
        searchbar.inputPlainText()
        searchbar.style.draw(width=400, height=40, moveX=20, moveY="50%",flipX=True)
        searchbar.style.roundCorners(all=20)
        searchbar.style.border(style="solid", width=1, color="#000000")
        searchbar.style.setOrigin(originY="-50%")
        searchbar.placeholder("  Search...")
        searchbar.style.font(size=20)
        topbox.searchbar = searchbar

        moduleTitle = RTitle()
        moduleTitle.displaytext = "Lorem Ipsum Dolor Sit Amet"
        moduleTitle.style.margin()
        moduleTitle.style.padding()
        moduleTitle.style.draw(moveX="50%", moveY="50%")
        moduleTitle.style.setOrigin(originX="-50%", originY="-50%")
        moduleTitle.style.font(size=50)
        topbox.moduleTitle = moduleTitle

        #
        # Sidebox layout
        #
        sidebox = RBox()
        sidebox.style.margin()
        sidebox.style.draw(width=230, height="calc(100% - 100px)", moveY=100)
        sidebox.style.border(style="solid", width=1, color="#000000")

        sidebox.style.colorize(background=rgba(255,255,255,0.75))
        sidebox.style.roundCorners(bottomright=20)

        from RTS_WebUIBuilder.presets.Button1 import ButtonLeftImage
        button = ButtonLeftImage(imageSource="/src/leftpointer.svg", text="Back to Homepage", width="calc(100% - 20px)")
        sidebox.titlebutton = button.button
        sidebox.titlebutton.style.draw(moveX=10, moveY=10)

        sidebox.buttongroup = RBox()
        self.topics = sidebox.buttongroup
        self.addTopics(docMemory.initDocs.topics, docMemory.initDocs.subtopics)
        sidebox.buttongroup.style.draw(width="calc(100% - 20px)", height="calc(100% - 55px)", moveY=45, moveX=10)

        
        

        #
        # Container layout
        #
        container = RBox()
        dom.body.container = container
        container.style.margin()
        container.style.draw(width="calc(100% - 242px)", height="calc(100% - 112px)", moveX=237, moveY=107)
        container.style.overflow(Y="auto")
        container.style.font(size=15)
        congrstyle = container.groupstyle = RGroupStyle(ident="*")    
        congrstyle.removeScrollbar()

 
        title = RTitle()
        title.displaytext = "Lorem Ipsum"
        title.style.alignment(align="center")
        title.style.margin(top=20)
        title.style.padding(bottom=10)
        #title.style.font(fontName="Roboto")
        title.style.border(style="solid", width=2, color="#000000", affected_sides="bottom")
        dom.body.container.title = title
    	

        
        dom.body.sidebox = sidebox
        dom.body.topbox = topbox
        self.container = dom.body.container

        
    def addTopics(self, topiclist:list[tuple[str,str]], subtopics:list[list[tuple[str,str]]] = None):
        from RTS_WebUIBuilder.presets.Button1 import ButtonLeftImage
        for (topic, pointer), subtopics_list in zip(topiclist, subtopics):
            if pointer.strip('/') == self._currentTopic:
                button = ButtonLeftImage(imageSource="/src/downpointer.svg", text=topic, width="100%", buttonBackground=rgba(0,0,0,0.2))
                button.button.style.draw(position="relative")
                button.button.clickEvent("redirect", f"'/docs/{self._modulename.lower()}{pointer}'")
                #print(f"'/docs/{self._modulename.lower()}{pointer}'")
                button.button.style.margin(top=5, bottom=10)
                setattr(self.topics, topic, button.button)

                for subtopic, subpointer in subtopics_list:
                    if subpointer.strip('/') == self._currentsub:
                        sbutton = ButtonLeftImage(imageSource="/src/rightpointer.svg", text=subtopic, width="calc(100% - 20px)", buttonBackground=rgba(0,0,0,0.3))
                    else:
                        sbutton = ButtonLeftImage(imageSource="/src/rightpointer.svg", text=subtopic, width="calc(100% - 20px)", buttonBackground=rgba(0,0,0,0.1))
                    sbutton.button.style.draw(position="relative",moveX=20)
                    sbutton.button.style.margin(top=5, bottom=10)
                    sbutton.button.clickEvent("redirect", f"'/docs/{self._modulename.lower()}{pointer}{subpointer}'")
                    #print(f"'/docs/{self._modulename.lower()}{pointer}{subpointer}'")
                    setattr(self.topics, subtopic, sbutton.button)
            else:
                button = ButtonLeftImage(imageSource="/src/rightpointer.svg", text=topic, width="100%")
                button.button.style.draw(position="relative")
                button.button.style.margin(top=5, bottom=10)
                button.button.clickEvent("redirect", f"'/docs/{self._modulename.lower()}{pointer}'")
                #print(f"'/docs/{self._modulename.lower()}{pointer}'")
                setattr(self.topics, topic, button.button)
    

    
    def addText(self,textname:str,text:str):
        if not isinstance(textname, str) or textname:
            #generate random string
            textname = ''.join(random.choice(string.ascii_letters) for _ in range(10))

        def colorize(token: str, color: str):
            lable = RLabel("span")
            lable.displaytext = token
            lable.style.colorize(color=color)
            return lable._asm()
        


        reformated_text = re.sub(r'\n', '</br>', text)
        reformated_text = re.sub(r'  ', '&nbsp;&nbsp;&nbsp;', reformated_text)
        reformated_text = re.sub(r'Note:', colorize("Note:", "yellow"), reformated_text)

        def replace_with_color(match):
            color = match.group(1)
            text = match.group(2)
            return colorize(text, color)

        reformated_text = re.sub(r'\$([\w#]+)\$(.*?);', replace_with_color, reformated_text)
        reformated_text = re.sub(r'\$([\w#]+)\$(.*?);', replace_with_color, reformated_text)


        codeblock = RLabel()
        codeblock.style.padding(top=20, bottom=20, left=20, right=20)
        codeblock.style.colorize(background=rgba(0,0,0,0.1))
        codeblock.style.roundCorners(all=20)
        codeblock.style.font(size=17)
        codeblock.style.overflow(X="auto")
        

        codeblock.style.draw(width="calc(100% - 40px)", height="auto", position="relative")
        codeblock.displaytext =  reformated_text

        setattr(self.container, textname, codeblock)

    


    def addCodeBlock(self, scriptname: str, code: str, filt:bool=False):
        from RTS_WebUIBuilder.RpyColorizer import pylexerColorizer

        if not isinstance(code, str):
            raise ValueError("code must be a string.")
        if not code:
            raise ValueError("code cannot be empty.")

        reformated_code = pylexerColorizer(code,filt)  # Färbe den Code ein
        if not isinstance(scriptname, str) or scriptname:
            #generate random string
            scriptname = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        codeblock = RLabel()
        codeblock.style.padding(top=20, bottom=20, left=20, right=20)
        codeblock.style.colorize(background=rgb(13, 17, 23))
        codeblock.style.roundCorners(all=20)
        
        codeblock.style.overflow(X="auto")
        

        codeblock.style.draw(width="calc(100% - 40px)", height="auto", position="relative")
        codeblock.displaytext = reformated_code  # Füge den eingefärbten Code hinzu

        setattr(self.container, scriptname, codeblock)

