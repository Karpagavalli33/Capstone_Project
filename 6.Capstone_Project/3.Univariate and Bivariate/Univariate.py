import pandas as pd
import numpy as np
class Univariate():
    def QuanQual(dataset):
        quan=[]
        qual=[]
        for ColumnName in dataset.columns:
            #print(ColumnName)
            if (dataset[ColumnName].dtypes=='O'):
                #print("qual")
                qual.append(ColumnName)
            else:
                #print("quan")
                quan.append(ColumnName)
        return quan,qual
        
    def descriptive(dataset, quan):
        import pandas as pd
        descriptive=pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","Q4:99%",
                                      "Q5:100%","IQR","1.5Rule","Lesser","Greater","Min","Max"],columns=quan)
        for ColumnName in quan:
            descriptive[ColumnName]["Mean"]=dataset[ColumnName].mean()
            descriptive[ColumnName]["Median"]=dataset[ColumnName].median()
            descriptive[ColumnName]["Mode"]=dataset[ColumnName].mode()[0]
            descriptive[ColumnName]["Q1:25%"]=dataset.describe()[ColumnName]["25%"]
            descriptive[ColumnName]["Q2:50%"]=dataset.describe()[ColumnName]["50%"]
            descriptive[ColumnName]["Q3:75%"]=dataset.describe()[ColumnName]["75%"]
            descriptive[ColumnName]["Q4:99%"]=np.percentile(dataset[ColumnName],99)
            descriptive[ColumnName]["Q5:100%"]=dataset.describe()[ColumnName]["max"]
            descriptive[ColumnName]["IQR"]= descriptive[ColumnName]["Q3:75%"]-descriptive[ColumnName]["Q1:25%"]
            descriptive[ColumnName]["1.5Rule"]=1.5*descriptive[ColumnName]["IQR"]
            descriptive[ColumnName]["Lesser"]=descriptive[ColumnName]["Q1:25%"]-descriptive[ColumnName]["1.5Rule"]
            descriptive[ColumnName]["Greater"]=descriptive[ColumnName]["Q3:75%"]+descriptive[ColumnName]["1.5Rule"]
            descriptive[ColumnName]["Min"]=dataset[ColumnName].min()
            descriptive[ColumnName]["Max"]=dataset[ColumnName].max()
            descriptive[ColumnName]["Kurtosis"]=dataset[ColumnName].kurtosis()
            descriptive[ColumnName]["Skewness"]=dataset[ColumnName].skew()
            descriptive[ColumnName]["Variance"]=dataset[ColumnName].var()
            descriptive[ColumnName]["Std_deviation"]=dataset[ColumnName].std()
        return descriptive
    def ftable(columnName,dataset):
        ftable=pd.DataFrame(columns=["Unique_values","Frequency","Relative_Frequency","Cumsum"])
        ftable["Unique_values"]=dataset[columnName].value_counts().index
        ftable["Frequency"]=dataset[columnName].value_counts().values
        ftable["Relative_Frequency"]=ftable["Frequency"]/103
        ftable["Cumsum"]=ftable["Relative_Frequency"].cumsum()
        return ftable
    def outlier(dataset,quan,descriptive):
        lesser=[]
        greater=[]
        for columnName in quan:
            if(descriptive[columnName]["Min"]<descriptive[columnName]["Lesser"]):
                lesser.append(columnName)
            if(descriptive[columnName]["Max"]>descriptive[columnName]["Greater"]):
                greater.append(columnName)
        return lesser,greater
    
    def replaceoutlier(dataset, lesser, greater, descriptive):
    # Replace outliers in the lesser range
        for columnName in lesser:
            dataset[columnName][dataset[columnName] < descriptive[columnName]["Lesser"]] = descriptive[columnName]["Lesser"]
        
        # Replace outliers in the greater range
        for columnName in greater:
            dataset[columnName][dataset[columnName] > descriptive[columnName]["Greater"]] = descriptive[columnName]["Greater"]
        
        return dataset
