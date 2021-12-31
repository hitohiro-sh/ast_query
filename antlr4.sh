DIR="$( cd "$( dirname "$0" )" && pwd )"

#echo $DIR

alias antlr4='java -Xmx500M -cp "$DIR/local/lib/antlr-4.9-complete.jar:$CLASSPATH" org.antlr.v4.Tool'
alias grun='java -Xmx500M -cp "$DIR/local/lib/antlr-4.9-complete.jar:$CLASSPATH" org.antlr.v4.gui.TestRig'

#echo "$@"

antlr4 $@
