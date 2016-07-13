package mapReduce_earthquake;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.fs.Path;



public class GetWeeklyForecast {

	public static class WeeklyMapper extends MapReduceBase
	implements Mapper <LongWritable, Text, Text, DoubleWritable> {

		@Override
		public void map(LongWritable key, Text value, OutputCollector<Text, DoubleWritable> output, Reporter rep) 
				throws IOException {
			
			//reading each line and splitting by ,
			String line = value.toString();
			String [] data = line.split(",");
		
			
			String str_date = data[0].substring(9,10);
			Integer date = Integer.parseInt(str_date);
			Double mag;
		
			if (data[4].toString() == null || data[4].isEmpty() ) {
				mag = 0.0;
			}
			else {
				mag = Double.parseDouble(data[4].toString());
			}
			
			// Split based on week
			if(date >= 1 && date < 8) {
				String week = "week 1";
				output.collect(new Text(week), new DoubleWritable(mag));
			}
			
			else if (date >= 8 && date < 15) {
				String week = "week 2";
				output.collect(new Text(week), new DoubleWritable(mag));
			}
			else if( date >= 15 && date < 22) {
				String week = "week 3";
				output.collect(new Text(week), new DoubleWritable(mag));
			}
			else if ( date >= 22 && date <29 ) {
				String week = "week 4";
				output.collect(new Text(week), new DoubleWritable(mag));
			}
			else if (date >=29 && date <=31 ) {
				String week = "week 5";
				output.collect(new Text(week), new DoubleWritable(mag));
			}
		}
	}
	public static class WeeklyReducer extends MapReduceBase 
	implements Reducer <Text, DoubleWritable, Text, DoubleWritable> {
		
		@Override
		public void reduce(Text key, Iterator<DoubleWritable> values,
				OutputCollector<Text, DoubleWritable> output, Reporter rep)
				throws IOException {
			double range = 0.0;
			while(values.hasNext()) {
				range = values.next().get();
				if(range >= 0.0  && range <= 2.0) {
					output.collect(key, new DoubleWritable(range));
				}
				
			}
			
		}
	}


	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
		// TODO Auto-generated method stub
		JobConf conf = new JobConf(GetDailyForecast.class); 
	      
	      conf.setJobName("weeklyMagAnalysis"); 
	      conf.setOutputKeyClass(Text.class);
	      conf.setOutputValueClass(DoubleWritable.class); 
	      conf.setMapperClass(WeeklyMapper.class); 
	      conf.setReducerClass(WeeklyReducer.class); 
	      conf.setInputFormat(TextInputFormat.class); 
	      conf.setOutputFormat(TextOutputFormat.class); 
	      
	      FileInputFormat.setInputPaths(conf, new Path(args[0])); 
	      FileOutputFormat.setOutputPath(conf, new Path(args[1])); 
	      
	      JobClient.runJob(conf); 
    
	}

}
