/*
 * This file contains a sample reader for paraview copied from a kitware tutorial.
 * It is for reading in image (i.e. cartesian) data from a ascii csv format
 */
 
 class vtkCSVImageReader: public vtkImageAlgorithm{
 public:
 	static vtkCSVImageReader* New();
 	vtkTypeRevisionMacro(vtkCSVImageReader, vtkImageAlgorithm);
 	void PrintSelf(ostream& os, vtkIndent indent);
 	
 	virtual void SetFileName(const char* fname);
 	virtual const char* GetFileName();
 	virtual void SetFieldDelimiterCharacters(const char* delim)
 	virtual const char* GetFieldDelimiterCharacters()
 	
 protected:
 	vtkCSVImageReader();
 	~vtkCSVImageReader();
 	
 	int RequestInformation(vtkInformation*, vtkInformationVector**, 
 	                       vtkInformationVector*);
 	int RequestData(vtkInformation*, vtkInformationVector**, 
 	                vtkInformationVector*);
 	
 	vtkDelimitedTextReader* Reader;
 	
 private:
 	vtkCSVImageReader(const vtkCSVImageReader&)
 	void operator=(const vtkCSVImageReader&)
 }
