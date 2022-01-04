
import java.io.IOException;
import java.util.function.BiConsumer;

import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.CharStreams;


public class Main {
    private static void tr(ParseTree tree, int depth, BiConsumer<String, Integer> func) {
        func.accept(tree.getClass().toString(), depth);
        for (int i = 0; i < tree.getChildCount(); i++) {
            var child = tree.getChild(i);
            tr(child, depth+1, func);
        }
    }
    public static void main(String[] args) {
        try {
            var input = CharStreams.fromFileName(args[0]);
            var lexer = new Python3Lexer(input);
            var stream = new CommonTokenStream(lexer);
            var parser = new Python3Parser(stream);
            var tree = parser.file_input();
            tr(tree, 0, (var str, var depth) -> {
                
                System.out.println(depth + ":" + str);
            });
        } catch (IOException ex) {
            System.err.println(ex);
        }


    }
}
