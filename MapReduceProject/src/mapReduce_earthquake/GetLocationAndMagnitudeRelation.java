package mapReduce_earthquake;
import java.io.IOException;
import java.util.*;

import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;

import org.apache.hadoop.fs.Path;



public class GetLocationAndMagnitudeRelation {
	
	public static class LocationMapper extends MapReduceBase
	implements Mapper <LongWritable, Text, Text, DoubleWritable> {
		@Override
		public void map(LongWritable key, Text value, OutputCollector<Text, DoubleWritable> output, Reporter rep) 
			throws IOException {
			
				//reading each line and splitting by ,
				String line = value.toString();
				String [] data = line.split(",");
				
				String location = data[21];
				Double mag;
				
				if (data[4].toString() == null || data[4].isEmpty() ) {
					mag = 0.0;
				}
				else {
					mag = Double.parseDouble(data[4].toString());
				}
				output.collect(new Text(location), new DoubleWritable(mag));
			}
		
		}
	
	
	public static class LocationReducer extends MapReduceBase
	implements Reducer <Text, DoubleWritable, Text, DoubleWritable> {
		
		@Override
		public void reduce(Text key, Iterator<DoubleWritable> values,
				OutputCollector<Text, DoubleWritable> output, Reporter rep)
				throws IOException {
					int count = 0;
					double range = 0.0;
					while(values.hasNext()) {
						count += 1;
						DoubleWritable val = values.next();
						range += val.get();
					}
					
					double avg = range/count;
					output.collect(key, new DoubleWritable(avg));
			}
		}
		
		@SuppressWarnings("resource")
		public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
			// TODO Auto-generated method stub
			JobConf conf = new JobConf(GetDailyForecast.class); 
			
			Scanner s = new Scanner(System.in);
		    System.out.print("\nEnter Number of mapper: ");
		    String map_count = s.next();
			System.out.println("User Input: " + map_count);
			
			System.out.print("\nEnter Number of reducer: ");
			String red_count = s.next();
			System.out.println("User Input: " + red_count);
			
		      conf.setJobName("locationMagAnalysis"); 
		      
		      //Set number of Mappers and Reducer
		      //conf.setNumMapTasks(Integer.parseInt(map_count));
		      //conf.setNumReduceTasks(Integer.parseInt(red_count)); 
		      
		      conf.setOutputKeyClass(Text.class);
		      conf.setOutputValueClass(DoubleWritable.class); 
		      
		      conf.setMapperClass(LocationMapper.class); 
		      conf.setReducerClass(LocationReducer.class); 
		      
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
