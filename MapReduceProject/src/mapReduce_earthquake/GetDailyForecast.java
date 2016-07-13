package mapReduce_earthquake;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;

import org.apache.hadoop.fs.Path;


public class GetDailyForecast {
	
	public static class DailyMapper extends MapReduceBase
	implements Mapper <LongWritable, Text, Text, DoubleWritable> {

		@Override
		public void map(LongWritable key, Text value, OutputCollector<Text, DoubleWritable> output, Reporter rep) 
				throws IOException {
			
			//reading each line and splitting by ,
			String line = value.toString();
			String [] data = line.split(",");
			
			System.out.println(data[0]);
			System.out.println(data[1]);
			System.out.println(data[2]);
			System.out.println(data[3]);
			System.out.println(data[4]);
			
			String str_date = data[0].substring(9,10);
			
			Double mag;
			//Integer date = Integer.parseInt(str_date);
			if (data[4].toString() == null || data[4].isEmpty() ) {
				mag = 0.0;
			}
			else {
				mag = Double.parseDouble(data[4].toString());
			}
			output.collect(new Text(str_date), new DoubleWritable(mag));
		}
	}
	public static class DailyReducer extends MapReduceBase 
	implements Reducer <Text, DoubleWritable, Text, DoubleWritable> {
		
		public DailyReducer() {}
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


	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
		// TODO Auto-generated method stub
		JobConf conf = new JobConf(GetDailyForecast.class); 
	      
	      conf.setJobName("dailyMagAnalysis"); 
	      conf.setOutputKeyClass(Text.class);
	      conf.setOutputValueClass(DoubleWritable.class); 
	      conf.setMapperClass(DailyMapper.class); 
	      conf.setReducerClass(DailyReducer.class); 
	      conf.setInputFormat(TextInputFormat.class); 
	      conf.setOutputFormat(TextOutputFormat.class); 
	      
	      FileInputFormat.setInputPaths(conf, new Path(args[0])); 
	      FileOutputFormat.setOutputPath(conf, new Path(args[1])); 
	      
	      JobClient.runJob(conf); 
    
	}

}
