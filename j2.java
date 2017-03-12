// ls target

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.Scanner;

public class j2
{
	private static final String SERVER_1="/space/home/jboss/appservers/liferay-portal-6.0-ee/tomcat-6.0.29/bin";
	private static final String ROOT="/";
	private static final String SPACE=ROOT+"space";
	private static final String HOME=SPACE+"/home";
	private static final String JBOSS=HOME+"/jboss";
	private static final String APPSERVERS=JBOSS+"/appservers";
	private static final String LIFERAY=APPSERVERS+"/liferay-portal-6.0-ee";
	private static final String TOMCAT_HOME=LIFERAY+"/tomcat-6.0.29";
	private static final String BIN=TOMCAT_HOME+"/bin";
	private static final String CONF=TOMCAT_HOME+"/conf";
	private static final String LIB=TOMCAT_HOME+"/lib";
	private static final String LOGS=TOMCAT_HOME+"/logs";
	private static final String TEMP=TOMCAT_HOME+"/temp";
	private static final String WEBAPPS=TOMCAT_HOME+"/webapps";
	private static final String WORK=TOMCAT_HOME+"/work";
	private String result;
	private StringWriter sw=null;

	public j2 ()
	{
		result="";
		Process p=null;

		try{
			p = Runtime.getRuntime().exec("ls -l "+WEBAPPS);

			if (p!=null){
				Scanner sc = new Scanner (p.getInputStream());
				while (sc.hasNextLine())
					result += sc.nextLine() + "\n";
			}

		}catch (IOException ioe){
			sw = new StringWriter ();
			ioe.printStackTrace(new PrintWriter(sw));
			result += sw.toString() + "\n";
		}
	}

	private void process (String trg)
	{
		process (new File (trg), 0);
	}

	private void process (File current, int level)
	{
		if (current.isDirectory())
		{
			File[] children = null;
			children = current.listFiles();
			if (children!=null){
				for (File child : children)
					result += child.getName() + "\n";
			}
		}
	}

	public String toString ()
	{
		return result;
	}
}
