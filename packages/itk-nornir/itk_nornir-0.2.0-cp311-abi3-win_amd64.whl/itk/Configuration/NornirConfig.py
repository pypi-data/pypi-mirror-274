depends = ('ITKPyBase', 'ITKStatistics', 'ITKImageSources', 'ITKCommon', )
templates = (  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridISS2ISS2', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridISS4ISS4', True, 'itk::Image< signed short,4 >, itk::Image< signed short,4 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridIUC2IUC2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridIUC4IUC4', True, 'itk::Image< unsigned char,4 >, itk::Image< unsigned char,4 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridIUS2IUS2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridIUS3IUS3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridIUS4IUS4', True, 'itk::Image< unsigned short,4 >, itk::Image< unsigned short,4 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridIF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridIF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridIF4IF4', True, 'itk::Image< float,4 >, itk::Image< float,4 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridID2ID2', True, 'itk::Image< double,2 >, itk::Image< double,2 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridID3ID3', True, 'itk::Image< double,3 >, itk::Image< double,3 >'),
  ('IRRefineGrid', 'itk::IRRefineGrid', 'itkIRRefineGridID4ID4', True, 'itk::Image< double,4 >, itk::Image< double,4 >'),
  ('MinimalStandardRandomVariateGenerator', 'itk::Statistics::MinimalStandardRandomVariateGenerator', 'itkMinimalStandardRandomVariateGenerator', True),
)
factories = ()
