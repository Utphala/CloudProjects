package mapReduce_earthquake;
import java.io.IOException;
import java.util.*;

import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.fs.Path;

public class GetSurvived {
	
	public static class SurviverMapper extends MapReduceBase
	implements Mapper <LongWritable, Text, Text, IntWritable> {
		@Override
		public void map(LongWritable key, Text value, OutputCollector<Text, IntWritable> output, Reporter rep) 
			throws IOException {
			
				//reading each line and splitting by ,
				String line = value.toString();
				String [] data = line.split(",");
				
				Double age;
				
				System.out.println(data[0]);
				System.out.println(data[1]);
				System.out.println(data[2]);
				System.out.println(data[3]);
				System.out.println(data[4]);
				
				if(data[5] == null || data[5].isEmpty())  {
					age = 0.0;
				}
				else {
					age = Double.parseDouble(data[5]);
				}

				if (age >= 0.0 && age < 1.0 )
				{
					String type = "Infant";
					output.collect(new Text(type), new IntWritable (Integer.parseInt(data[0])));
				}
				else if (age >= 1.0 && age < 15.0)
				{
					String type = "Child";
					output.collect(new Text(type), new IntWritable (Integer.parseInt(data[0])));
				}
				else if (age >= 15 && age < 100)
				{
					String type = "Adult";
					output.collect(new Text(type), new IntWritable (Integer.parseInt(data[0])));
				}
		}
	}
	
	public static class SurviverReducer extends MapReduceBase
	implements Reducer < Text, IntWritable, Text, IntWritable> {
		
		@Override
		public void reduce(Text key, Iterator<IntWritable> values,
				OutputCollector<Text, IntWritable> output, Reporter rep)
				throws IOException {
					Integer count = 0;
				
					while(values.hasNext()) {
						
						count += 1;
					}
					
					output.collect(key, new IntWritable(count));
			}
		}
	
	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
		// TODO Auto-generated method stub
		JobConf conf = new JobConf(GetDailyForecast.class); 
		
		/** Scanner s = new Scanner(System.in);
	    System.out.print("\nEnter Number of mapper: ");
	    String map_count = s.next();
		System.out.println("User Input: " + map_count);
		
		System.out.print("\nEnter Number of reducer: ");
		String red_count = s.next();
		System.out.println("User Input: " + red_count);*/
		
	      conf.setJobName("SurviverAnalysis"); 
	      
	      //Set number of Mappers and Reducer
	      conf.setNumMapTasks(4);
	      conf.setNumReduceTasks(1); 
	      
	      conf.setOutputKeyClass(Text.class);
	      conf.setOutputValueClass(IntWritable.class); 
	      
	      conf.setMapperClass(SurviverMapper.class); 
	      conf.setReducerClass(SurviverReducer.class); 
	      
	      conf.setInputFormat(TextInputFormat.class); 
	      conf.setOutputFormat(TextOutputFormat.class); 
	      
	      FileInputFormat.setInputPaths(conf, new Path(args[0])); 
	      FileOutputFormat.setOutputPath(conf, new Path(args[1])); 
	      
	  	  //calling the run method and calculating time
		  long StartTime = System.currentTimeMillis();
		  
	      JobClient.runJob(conf); 
	      
	      long EstimatedTime = System.currentTimeMillis() - StartTime;
	      System.out.println("Time taken: "+EstimatedTime+ " ms");
	}
	
}