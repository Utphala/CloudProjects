
 palette(c("#E41A1C", "#377EB8", "#4DAF4A", "#984EA3",
          "#FF7F00", "#FFFF33", "#A65628", "#F781BF", "#999999"))

myData <- read.csv("Data(1).csv")
nums <- sapply(myData, is.numeric)
myData <- myData[,nums]

shinyServer(function(input, output, session) {
  
  # Combine the selected variables into a new data frame
  selectedData <- reactive({                                # Reactive acts as "event-listener" 
    myData[, c(input$xval, input$yval)]                     # listening for changes 
  })

  clusters <- reactive({
    kmeans(selectedData(), input$clusters)
  })
 
   output$plot1 <- renderPlot({
    par(mar = c(5.1, 4.1, 0, 1))
    plot(selectedData(),
         col = clusters()$cluster,
         pch = 20, cex = 3
    )
    
  points(clusters()$centers, pch = 3, cex = 4, lwd = 3)
  print(clusters()$centers)
  print(clusters()$size)

  output$plot2 <- renderPlot({
    barplot(clusters()$centers, width = 6, space = NULL , names.arg = NULL, legend.text = NULL, beside = TRUE,
            horiz = FALSE, density = NULL, angle = 45,
            col = NULL, border = par("fg"),
            main = NULL, sub = NULL, xlab="Number of clusters", ylab="Centriods",xlim = NULL, ylim = NULL, xpd = TRUE, log = "",
            axes = TRUE, axisnames = TRUE,
            cex.axis = par("cex.axis"), cex.names = par("cex.axis"),
            inside = TRUE, plot = TRUE, axis.lty = 0, offset = 0,
            add = FALSE, args.legend = NULL)
  })


  output$plot3 <- renderText({
    
    str2 <- c("Centers are: ",clusters()$centers)
    str2
  })
  
})

