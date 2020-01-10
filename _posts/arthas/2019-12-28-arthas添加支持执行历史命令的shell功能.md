---
layout: post
title: arthas github commit 
categories: [java,arthas,性能调优,jvm]
description: 增加历史命令。
keywords: 在线性能调优 , arthas , jvm
---

arthas是阿里开源的线上性能调优利器,有中文文档可供参考学习,https://alibaba.github.io/arthas/install-detail.html

## 提交github commit 

添加执行历史命令的支持,使用叹号+历史命令数字,符合linux用户的shell习惯

类 com.taobao.arthas.core.shell.system.impl.JobControllerImpl#createProcess
添加支持执行历史命令的shell功能

git checkout -b arthas_add_exec_histroy_command
git add core/src/main/java/com/taobao/arthas/core/shell/system/impl/JobControllerImpl.java
git commit -m "添加叹号执行历史命令功能,例子:!33"

```java
修改添加英文注释
 com.taobao.arthas.core.shell.system.impl.JobControllerImpl#createProcess
 /**
     * Try to create a process from the command line tokens.
     *
     * @param line           the command line tokens
     * @param commandManager command manager
     * @param jobId          job id
     * @param term           term
     * @return the created process
     */
    private Process createProcess(List<CliToken> line, InternalCommandManager commandManager, int jobId, Term term) {
        try {
            ListIterator<CliToken> tokens = line.listIterator();
            while (tokens.hasNext()) {
                CliToken token = tokens.next();
                 //if the input string start with "!"
                if (token.isText() && (token.value().startsWith(EXCLAMATION_MARK))) {
                    //wipe off the  "!" & blank
                    String historyId = token.value().substring(1).trim();
                    //obtain commandName from history list
                    String commandName = getCommandName( term, Integer.valueOf(historyId));

                    // if the history command still contains the "!" , such as "!!40"
                    while (commandName!=null && commandName.startsWith(EXCLAMATION_MARK)){
                        commandName= getCommandName( term,Integer.valueOf(commandName.substring(1)) );
                    }

                    //command with args eg: 33 sc com.taobao.arthas.core.shell.system.impl.JobControllerImpl
                    if(commandName.contains("\u0020")){
                        return createProcess(CliTokens.tokenize(commandName),commandManager,jobId,term);
                    }

                    //command with out args, obtain command Object from the CommandManager
                    Command command = commandManager.getCommand(commandName);
                    if (command != null) {
                        //create the CommandProcess
                        return createCommandProcess(command, tokens, jobId, term);
                    } else {
                        throw new IllegalArgumentException(commandName + ": history command not found");
                    }
                }
                if (token.isText()) {
                    Command command = commandManager.getCommand(token.value());
                    if (command != null) {
                        return createCommandProcess(command, tokens, jobId, term);
                    } else {
                        throw new IllegalArgumentException(token.value() + ": command not found");
                    }
                }
            }
            throw new IllegalArgumentException();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
 
 /**
     * obtain commandName from history list
     * @param termObject  terminal Object
     * @param historyId the number input after the "!"
     * @return CommandName
     */
    private String getCommandName(Term termObject, int historyId) {
        if (termObject != null && termObject instanceof TermImpl) {
            TermImpl term = (TermImpl) termObject;
            Readline readline = term.getReadline();
            List<int[]> history = readline.getHistory();
            StringBuilder sb = new StringBuilder();
            int size = history.size();
            if(historyId>size){
                throw new IllegalArgumentException(historyId+" is to big, please input the right number,less than "+size);
            }
            int[] line = history.get(size - historyId);
            Helper.appendCodePoints(line, sb);
            return sb.toString().trim();
        }

        return null;
    }
    
    
  中文注释  
    //如果是叹号开头
if (token.isText() && (token.value().startsWith("!"))) {
    //throw new IllegalArgumentException(token.value() + ": find History Command");
    String historyId = token.value().substring(1); //去除第一个叹号
    String commandName = getCommandName( term, historyId).trim();
   // throw new IllegalArgumentException(commandName + ": find History Command");
    while (commandName.startsWith("!")){ //如果历史命令中还有！开头的
        commandName= getCommandName( term, commandName.substring(1)).trim();
    }
    //根据历史命令获取命令对象
    Command command = commandManager.getCommand(commandName);
    if (command != null) {
        //传教命令进程
        return createCommandProcess(command, tokens, jobId, term);
    } else {
        throw new IllegalArgumentException(token.value() + ": history command not found");
    }
}
```