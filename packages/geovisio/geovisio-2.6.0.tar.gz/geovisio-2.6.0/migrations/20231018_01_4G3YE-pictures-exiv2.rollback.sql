-- pictures-exiv2
-- depends: 20230803_01_aXusm-fix-sequence-computed

-- Temporary removal of update trigger
DROP TRIGGER pictures_update_sequences_trg ON pictures;

-- Restore old naming
UPDATE pictures SET exif = jsonb_build_object(
	'ProcessingSoftware', exif->'Exif.Image.ProcessingSoftware',
	'ImageWidth', exif->'Exif.Image.ImageWidth',
	'ImageLength', exif->'Exif.Image.ImageLength',
	'ImageDescription', exif->'Exif.Image.ImageDescription',
	'Make', exif->'Exif.Image.Make',
	'Model', exif->'Exif.Image.Model',
	'Orientation', exif->'Exif.Image.Orientation',
	'XResolution', exif->'Exif.Image.XResolution',
	'YResolution', exif->'Exif.Image.YResolution',
	'ResolutionUnit', exif->'Exif.Image.ResolutionUnit',
	'Software', exif->'Exif.Image.Software',
	'DateTime', exif->'Exif.Image.DateTime',
	'Artist', exif->'Exif.Image.Artist',
	'YCbCrPositioning', exif->'Exif.Image.YCbCrPositioning',
	'Copyright', exif->'Exif.Image.Copyright',
	'ExposureTime', exif->'Exif.Image.ExposureTime',
	'FNumber', exif->'Exif.Image.FNumber',
	'ExposureProgram', exif->'Exif.Image.ExposureProgram',
	'ISOSpeedRatings', exif->'Exif.Image.ISOSpeedRatings',
	'DateTimeOriginal', exif->'Exif.Image.DateTimeOriginal',
	'CompressedBitsPerPixel', exif->'Exif.Image.CompressedBitsPerPixel',
	'ShutterSpeedValue', exif->'Exif.Image.ShutterSpeedValue',
	'ApertureValue', exif->'Exif.Image.ApertureValue',
	'BrightnessValue', exif->'Exif.Image.BrightnessValue',
	'ExposureBiasValue', exif->'Exif.Image.ExposureBiasValue',
	'MaxApertureValue', exif->'Exif.Image.MaxApertureValue',
	'SubjectDistance', exif->'Exif.Image.SubjectDistance',
	'MeteringMode', exif->'Exif.Image.MeteringMode',
	'LightSource', exif->'Exif.Image.LightSource',
	'Flash', exif->'Exif.Image.Flash',
	'FocalLength', exif->'Exif.Image.FocalLength',
	'FlashEnergy', exif->'Exif.Image.FlashEnergy',
	'FocalPlaneXResolution', exif->'Exif.Image.FocalPlaneXResolution',
	'FocalPlaneYResolution', exif->'Exif.Image.FocalPlaneYResolution',
	'FocalPlaneResolutionUnit', exif->'Exif.Image.FocalPlaneResolutionUnit',
	'ExposureIndex', exif->'Exif.Image.ExposureIndex',
	'SensingMethod', exif->'Exif.Image.SensingMethod'
) || jsonb_build_object(
	'PrintImageMatching', exif->'Exif.Image.PrintImageMatching',
	'UniqueCameraModel', exif->'Exif.Image.UniqueCameraModel',
	'LocalizedCameraModel', exif->'Exif.Image.LocalizedCameraModel',
	'BaselineSharpness', exif->'Exif.Image.BaselineSharpness',
	'MakerNoteSafety', exif->'Exif.Image.MakerNoteSafety',
	'ProfileCopyright', exif->'Exif.Image.ProfileCopyright',
	'PreviewColorSpace', exif->'Exif.Image.PreviewColorSpace',
	'PreviewDateTime', exif->'Exif.Image.PreviewDateTime',
	'ExposureTime', exif->'Exif.Photo.ExposureTime',
	'FNumber', exif->'Exif.Photo.FNumber',
	'ExposureProgram', exif->'Exif.Photo.ExposureProgram',
	'ISOSpeedRatings', exif->'Exif.Photo.ISOSpeedRatings',
	'SensitivityType', exif->'Exif.Photo.SensitivityType',
	'StandardOutputSensitivity', exif->'Exif.Photo.StandardOutputSensitivity',
	'RecommendedExposureIndex', exif->'Exif.Photo.RecommendedExposureIndex',
	'ExifVersion', exif->'Exif.Photo.ExifVersion',
	'DateTimeOriginal', exif->'Exif.Photo.DateTimeOriginal',
	'DateTimeDigitized', exif->'Exif.Photo.DateTimeDigitized',
	'OffsetTime', exif->'Exif.Photo.OffsetTime',
	'OffsetTimeOriginal', exif->'Exif.Photo.OffsetTimeOriginal',
	'OffsetTimeDigitized', exif->'Exif.Photo.OffsetTimeDigitized',
	'ComponentsConfiguration', exif->'Exif.Photo.ComponentsConfiguration',
	'CompressedBitsPerPixel', exif->'Exif.Photo.CompressedBitsPerPixel',
	'ShutterSpeedValue', exif->'Exif.Photo.ShutterSpeedValue',
	'ApertureValue', exif->'Exif.Photo.ApertureValue',
	'BrightnessValue', exif->'Exif.Photo.BrightnessValue',
	'ExposureBiasValue', exif->'Exif.Photo.ExposureBiasValue',
	'MaxApertureValue', exif->'Exif.Photo.MaxApertureValue',
	'SubjectDistance', exif->'Exif.Photo.SubjectDistance',
	'MeteringMode', exif->'Exif.Photo.MeteringMode',
	'LightSource', exif->'Exif.Photo.LightSource',
	'Flash', exif->'Exif.Photo.Flash',
	'FocalLength', exif->'Exif.Photo.FocalLength',
	'MakerNote', exif->'Exif.Photo.MakerNote',
	'UserComment', exif->'Exif.Photo.UserComment',
	'FlashpixVersion', exif->'Exif.Photo.FlashpixVersion',
	'ColorSpace', exif->'Exif.Photo.ColorSpace',
	'FlashEnergy', exif->'Exif.Photo.FlashEnergy',
	'FocalPlaneXResolution', exif->'Exif.Photo.FocalPlaneXResolution',
	'FocalPlaneYResolution', exif->'Exif.Photo.FocalPlaneYResolution',
	'FocalPlaneResolutionUnit', exif->'Exif.Photo.FocalPlaneResolutionUnit'
) || jsonb_build_object(
	'ExposureIndex', exif->'Exif.Photo.ExposureIndex',
	'SensingMethod', exif->'Exif.Photo.SensingMethod',
	'FileSource', exif->'Exif.Photo.FileSource',
	'SceneType', exif->'Exif.Photo.SceneType',
	'CustomRendered', exif->'Exif.Photo.CustomRendered',
	'ExposureMode', exif->'Exif.Photo.ExposureMode',
	'WhiteBalance', exif->'Exif.Photo.WhiteBalance',
	'DigitalZoomRatio', exif->'Exif.Photo.DigitalZoomRatio',
	'FocalLengthIn35mmFilm', exif->'Exif.Photo.FocalLengthIn35mmFilm',
	'SceneCaptureType', exif->'Exif.Photo.SceneCaptureType',
	'GainControl', exif->'Exif.Photo.GainControl',
	'Contrast', exif->'Exif.Photo.Contrast',
	'Saturation', exif->'Exif.Photo.Saturation',
	'Sharpness', exif->'Exif.Photo.Sharpness',
	'DeviceSettingDescription', exif->'Exif.Photo.DeviceSettingDescription',
	'SubjectDistanceRange', exif->'Exif.Photo.SubjectDistanceRange',
	'ImageUniqueID', exif->'Exif.Photo.ImageUniqueID',
	'BodySerialNumber', exif->'Exif.Photo.BodySerialNumber',
	'LensSpecification', exif->'Exif.Photo.LensSpecification',
	'LensMake', exif->'Exif.Photo.LensMake',
	'LensModel', exif->'Exif.Photo.LensModel',
	'SourceExposureTimesOfCompositeImage', exif->'Exif.Photo.SourceExposureTimesOfCompositeImage',
	'RelatedImageWidth', exif->'Exif.Iop.RelatedImageWidth',
	'RelatedImageLength', exif->'Exif.Iop.RelatedImageLength',
	'GPSVersionID', exif->'Exif.GPSInfo.GPSVersionID',
	'GPSLatitudeRef', exif->'Exif.GPSInfo.GPSLatitudeRef',
	'GPSLatitude', exif->'Exif.GPSInfo.GPSLatitude',
	'GPSLongitudeRef', exif->'Exif.GPSInfo.GPSLongitudeRef',
	'GPSLongitude', exif->'Exif.GPSInfo.GPSLongitude',
	'GPSAltitudeRef', exif->'Exif.GPSInfo.GPSAltitudeRef',
	'GPSAltitude', exif->'Exif.GPSInfo.GPSAltitude',
	'GPSTimeStamp', exif->'Exif.GPSInfo.GPSTimeStamp',
	'GPSStatus', exif->'Exif.GPSInfo.GPSStatus',
	'GPSMeasureMode', exif->'Exif.GPSInfo.GPSMeasureMode',
	'GPSDOP', exif->'Exif.GPSInfo.GPSDOP',
	'GPSSpeedRef', exif->'Exif.GPSInfo.GPSSpeedRef',
	'GPSSpeed', exif->'Exif.GPSInfo.GPSSpeed'
) || jsonb_build_object(
	'GPSTrackRef', exif->'Exif.GPSInfo.GPSTrackRef',
	'GPSTrack', exif->'Exif.GPSInfo.GPSTrack',
	'GPSImgDirectionRef', exif->'Exif.GPSInfo.GPSImgDirectionRef',
	'GPSImgDirection', exif->'Exif.GPSInfo.GPSImgDirection',
	'GPSMapDatum', exif->'Exif.GPSInfo.GPSMapDatum',
	'GPSProcessingMethod', exif->'Exif.GPSInfo.GPSProcessingMethod',
	'GPSDateStamp', exif->'Exif.GPSInfo.GPSDateStamp',
	'GPSDifferential', exif->'Exif.GPSInfo.GPSDifferential',
	'MPFNumberOfImages', exif->'Exif.MpfInfo.MPFNumberOfImages',
	'MPFPanOrientation', exif->'Exif.MpfInfo.MPFPanOrientation',
	'GPano:UsePanoramaViewer', exif->'Xmp.GPano.UsePanoramaViewer',
	'GPano:CaptureSoftware', exif->'Xmp.GPano.CaptureSoftware',
	'GPano:StitchingSoftware', exif->'Xmp.GPano.StitchingSoftware',
	'GPano:ProjectionType', exif->'Xmp.GPano.ProjectionType',
	'GPano:PoseHeadingDegrees', exif->'Xmp.GPano.PoseHeadingDegrees',
	'GPano:PosePitchDegrees', exif->'Xmp.GPano.PosePitchDegrees',
	'GPano:PoseRollDegrees', exif->'Xmp.GPano.PoseRollDegrees',
	'GPano:InitialViewHeadingDegrees', exif->'Xmp.GPano.InitialViewHeadingDegrees',
	'GPano:InitialViewPitchDegrees', exif->'Xmp.GPano.InitialViewPitchDegrees',
	'GPano:InitialViewRollDegrees', exif->'Xmp.GPano.InitialViewRollDegrees',
	'GPano:InitialHorizontalFOVDegrees', exif->'Xmp.GPano.InitialHorizontalFOVDegrees',
	'GPano:FirstPhotoDate', exif->'Xmp.GPano.FirstPhotoDate',
	'GPano:LastPhotoDate', exif->'Xmp.GPano.LastPhotoDate',
	'GPano:SourcePhotosCount', exif->'Xmp.GPano.SourcePhotosCount',
	'GPano:ExposureLockUsed', exif->'Xmp.GPano.ExposureLockUsed',
	'GPano:CroppedAreaImageWidthPixels', exif->'Xmp.GPano.CroppedAreaImageWidthPixels',
	'GPano:CroppedAreaImageHeightPixels', exif->'Xmp.GPano.CroppedAreaImageHeightPixels',
	'GPano:FullPanoWidthPixels', exif->'Xmp.GPano.FullPanoWidthPixels',
	'GPano:FullPanoHeightPixels', exif->'Xmp.GPano.FullPanoHeightPixels',
	'GPano:CroppedAreaLeftPixels', exif->'Xmp.GPano.CroppedAreaLeftPixels',
	'GPano:CroppedAreaTopPixels', exif->'Xmp.GPano.CroppedAreaTopPixels',
	'GPano:InitialCameraDolly', exif->'Xmp.GPano.InitialCameraDolly'
);

-- Restore trigger
CREATE TRIGGER pictures_update_sequences_trg
AFTER UPDATE ON pictures
REFERENCING OLD TABLE AS old_table NEW TABLE AS new_table
FOR EACH STATEMENT EXECUTE FUNCTION pictures_update_sequence();
