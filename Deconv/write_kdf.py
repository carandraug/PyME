from scipy import *
from scipy.io import *

def WriteKhorosHeader(fid, Date, TypeString, ValueDimX, ValueDimY, ValueDimZ, ValueDimE, ValueDimT):


  #if (ValueDimX <= 0 );  ValueDimX=1; end
  #if (ValueDimY <= 0 );  ValueDimY=1; end
  #if (ValueDimZ <= 0 );  ValueDimZ=1; end
  #if (ValueDimE <= 0 );  ValueDimE=1; end

  MagicNumVer = '\x01\x03\x13\x5E\x00\x02';
  
  MachineType = '\x41';   # This is PC format
  
  NumSets = 1
  NumBlocks = 2

  ObjAttrName =''
  ObjSegNr = 2

  SegAttrName = 'date'
  SegAttrNum = 1

  DateDim = 1
  DateType = 'String'
  EOA = '<>'            # end of attribute tag

  Seg2AttrName = 'locationGrid'
  Seg2AttrNum = 1

  LocationDim = 1
  LocationType = 'Integer'
  Location = 0
  EOA2 ='<>'            # end of attribute tag

  ValueAttrName ='value'
  ValueAttrNum = 0

  ValueDim = 5
  # const int  ValueDimT = 1;
  ValueOrder = [2,3,4,5,6]
  FixedDim = -1 
  FixedIndex = -1

  fid.write(MagicNumVer, 'b')
  fid.write(MachineType,'uchar')
  fid.write(NumSets, 'int32')
  fid.write(NumBlocks, 'int32')

  fid.write(ObjAttrName + '\0', 'uchar')
  fid.write(ObjSegNr, 'int32');

  fid.write(SegAttrName + '\0', 'uchar');
  fid.write(SegAttrNum, 'int32');
  fid.write(DateDim, 'int32');
  fid.write(DateType + '\0', 'uchar');
  
  #to->write((char *) Date,strlen(Date)+1);
  fid.write(Date + '\0', 'uchar');
  
  fid.write(EOA + '\0', 'uchar');

  fid.write(Seg2AttrName + '\0', 'uchar');
  fid.write(Seg2AttrNum, 'int32');
  fid.write(LocationDim, 'int32');
  fid.write(LocationType + '\0', 'uchar');
  fid.write(Location, 'int32');
  fid.write(EOA2 + '\0', 'uchar');

  fid.write(ValueAttrName + '\0', 'uchar');
  fid.write(ValueAttrNum, 'int32');
  fid.write(ValueDim, 'int32');
  
  #to->write((char *) TypeString,strlen(TypeString)+1);
  fid.write(TypeString + '\0', 'uchar');
  
  fid.write(ValueDimX, 'int32');
  fid.write(ValueDimY, 'int32');
  fid.write(ValueDimZ, 'int32');
  fid.write(ValueDimT, 'int32');
  fid.write(ValueDimE, 'int32');
  for i in range(5):
    fid.write(ValueOrder[i], 'int32');
  

  fid.write(FixedDim, 'int32');
  fid.write(FixedIndex, 'int32');

      
      
def WriteKhorosData(fname, d):
    
    fid = fopen(fname, 'w');
    
    siz = ones(5)
    
    siz2 = shape(d)
    
    siz[0:len(siz2)] = siz2
    
    (DimX,DimY,DimZ,DimE, DimT) = siz
    
    if (d.typecode() == 'b'):           
        TypeString = 'Unsigned Byte'
    elif (d.typecode() == 'i'):       
        TypeString = 'Integer'
    elif (d.typecode() == 'l'):       
        TypeString = 'Long'
    elif (d.typecode() == 'f'):      
        TypeString = 'Float' 
    elif (d.typecode() == 'd'):      
        TypeString = 'Double' 
    elif (d.typecode() == 'w'):      
        TypeString = 'Unsigned Short'
    else:
        fid.close()
        print 'Dont know about %ss ... fixme' % (d.typecode(),)
        error()
    
    
    WriteKhorosHeader(fid, 'hello', TypeString, DimX, DimY, DimZ, DimE, DimT)
    
    
    #fid.write(d)
    
    #for i in range(DimE):
    for j in range(DimZ):
        for k in range(DimY):
            #for l in range(DimX):
            a = fid.fwrite(d[:,k,j], d.typecode())
    
    fid.close()
    
    return