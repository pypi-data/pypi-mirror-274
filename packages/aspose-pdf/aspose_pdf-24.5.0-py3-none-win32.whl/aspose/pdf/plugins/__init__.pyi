﻿import aspose.pdf
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable

class ChatCompletion:
    
    def __init__(self):
        ...
    
    @property
    def id(self) -> str:
        ...
    
    @id.setter
    def id(self, value: str):
        ...
    
    @property
    def object(self) -> str:
        ...
    
    @object.setter
    def object(self, value: str):
        ...
    
    @property
    def created(self) -> int:
        ...
    
    @created.setter
    def created(self, value: int):
        ...
    
    @property
    def model(self) -> str:
        ...
    
    @model.setter
    def model(self, value: str):
        ...
    
    @property
    def choices(self) -> None:
        ...
    
    @choices.setter
    def choices(self, value: None):
        ...
    
    @property
    def usage(self) -> aspose.pdf.plugins.Usage:
        ...
    
    @usage.setter
    def usage(self, value: aspose.pdf.plugins.Usage):
        ...
    
    @property
    def system_fingerprint(self) -> str:
        ...
    
    @system_fingerprint.setter
    def system_fingerprint(self, value: str):
        ...
    
    ...

class Choice:
    
    def __init__(self):
        ...
    
    @property
    def index(self) -> int:
        ...
    
    @index.setter
    def index(self, value: int):
        ...
    
    @property
    def message(self) -> aspose.pdf.plugins.Message:
        ...
    
    @message.setter
    def message(self, value: aspose.pdf.plugins.Message):
        ...
    
    @property
    def finish_reason(self) -> str:
        ...
    
    @finish_reason.setter
    def finish_reason(self, value: str):
        ...
    
    ...

class CompressOptions(aspose.pdf.plugins.OrganizerBaseOptions):
    '''Represents Compress options for :class:`Optimizer` plugin.'''
    
    def __init__(self):
        ...
    
    ...

class DecryptionOptions(aspose.pdf.plugins.OrganizerBaseOptions):
    '''Represents Decryption Options for :class:`Security` plugin.'''
    
    def __init__(self, owner_password: str):
        '''Initializes new instance of the :class:`DecryptionOptions` object with default options.
        
        :param owner_password: Owner password.'''
        ...
    
    @property
    def owner_password(self) -> str:
        '''Owner password.'''
        ...
    
    @owner_password.setter
    def owner_password(self, value: str):
        ...
    
    ...

class EncryptionOptions(aspose.pdf.plugins.OrganizerBaseOptions):
    '''Represents Encryption Options for :class:`Security` plugin.'''
    
    def __init__(self, owner_password: str, user_password: str, document_privilege: aspose.pdf.facades.DocumentPrivilege, crypto_algorithm: aspose.pdf.CryptoAlgorithm):
        '''Initializes new instance of the :class:`EncryptionOptions` object with default options.
        
        :param owner_password: Owner password.
        :param user_password: User password.
        :param document_privilege: Document permissions.
        :param crypto_algorithm: Cryptographic algorithm.'''
        ...
    
    @property
    def owner_password(self) -> str:
        '''Owner password.'''
        ...
    
    @owner_password.setter
    def owner_password(self, value: str):
        ...
    
    @property
    def user_password(self) -> str:
        '''User password.'''
        ...
    
    @user_password.setter
    def user_password(self, value: str):
        ...
    
    @property
    def document_privilege(self) -> aspose.pdf.facades.DocumentPrivilege:
        '''Document permissions, see :class:`aspose.pdf.Permissions` for details.'''
        ...
    
    @document_privilege.setter
    def document_privilege(self, value: aspose.pdf.facades.DocumentPrivilege):
        ...
    
    @property
    def crypto_algorithm(self) -> aspose.pdf.CryptoAlgorithm:
        '''Cryptographic algorithm, see :attr:`EncryptionOptions.crypto_algorithm` for details.'''
        ...
    
    @crypto_algorithm.setter
    def crypto_algorithm(self, value: aspose.pdf.CryptoAlgorithm):
        ...
    
    ...

class FileDataSource:
    '''Represents file data source for load and save operations of a plugin.'''
    
    def __init__(self, path: str):
        '''Initializes new file data source with the specified path.
        
        :param path: A string representing the path to the source file.'''
        ...
    
    @property
    def data_type(self) -> None:
        '''Type of data source (file).'''
        ...
    
    @property
    def path(self) -> str:
        '''Gets the path to the file of the current data source.'''
        ...
    
    ...

class FileResult:
    '''Represents operation result in the form of string path to file.'''
    
    def to_file(self) -> str:
        '''Tries to convert the result to a file.
        
        :returns: A string representing the path to the output file if the result is file; otherwise ``None``.'''
        ...
    
    def to_stream(self) -> Any:
        '''Tries to convert the result to a stream object.
        
        :returns: A stream object representing the output data if the result is stream; otherwise ``None``.'''
        ...
    
    @property
    def is_file(self) -> bool:
        '''Indicates whether the result is a path to an output file.
        
        :returns: ``True`` if the result is a file; otherwise ``False``.'''
        ...
    
    @property
    def is_stream(self) -> bool:
        '''Indicates whether the result is an output stream.
        
        :returns: ``True`` if the result is a stream object; otherwise ``False``.'''
        ...
    
    @property
    def is_string(self) -> bool:
        '''Indicates whether the result is a text string.
        
        :returns: ``True`` if the result is a string; otherwise ``False``.'''
        ...
    
    @property
    def data(self) -> object:
        '''Gets raw data.
        
        :returns: An ``object`` representing output data.'''
        ...
    
    ...

class FormCheckBoxFieldCreateOptions(aspose.pdf.plugins.FormFieldCreateOptions):
    '''Represents options for creating CheckBoxField by FormEditor plugin.'''
    
    def __init__(self, page_num: int, rect: aspose.pdf.Rectangle):
        '''Initializes a new instance of the :class:`FormCheckBoxFieldCreateOptions` object, that containing parameters for created and added CheckBoxField.
        
        :param page_num: Page number on which the added CheckBoxField will be located.
        :param rect: Sets CheckBoxField rectangle.'''
        ...
    
    @property
    def checked(self) -> bool:
        '''Gets/sets the value to determine whether created CheckboxField is checked or not (if will be set).'''
        ...
    
    @checked.setter
    def checked(self, value: bool):
        ...
    
    @property
    def style(self) -> aspose.pdf.forms.BoxStyle:
        '''Gets/sets the value to determine property Style for created CheckboxField (if will be set).'''
        ...
    
    @style.setter
    def style(self, value: aspose.pdf.forms.BoxStyle):
        ...
    
    ...

class FormCheckBoxFieldSetOptions(aspose.pdf.plugins.FormFieldSetOptions):
    '''Represents options for set properties in CheckboxField by :class:`FormEditor` plugin.'''
    
    def __init__(self):
        ...
    
    @property
    def checked(self) -> bool:
        '''Gets/sets the value to determine property Checked for modified field (if will be set).'''
        ...
    
    @checked.setter
    def checked(self, value: bool):
        ...
    
    @property
    def style(self) -> aspose.pdf.forms.BoxStyle:
        '''Gets/sets the value to determine property BoxStyle for modified field (if will be set).'''
        ...
    
    @style.setter
    def style(self, value: aspose.pdf.forms.BoxStyle):
        ...
    
    ...

class FormComboBoxFieldCreateOptions(aspose.pdf.plugins.FormFieldCreateOptions):
    '''Represents options for creating ComboBoxField by :class:`FormEditor` plugin.'''
    
    def __init__(self, page_num: int, rect: aspose.pdf.Rectangle):
        '''Initializes a new instance of the :class:`FormComboBoxFieldCreateOptions` object, that containing parameters for created and added ComboBoxField.
        
        :param page_num: Page number on which the added ComboBoxField will be located.
        :param rect: Sets ComboBoxField rectangle.'''
        ...
    
    @property
    def editable(self) -> bool:
        '''Gets/sets the value to determine whether created ComboBoxField is editable or not (if will be set).'''
        ...
    
    @editable.setter
    def editable(self, value: bool):
        ...
    
    @property
    def options(self) -> None:
        '''Gets/sets the value to determine property Options for created ComboBoxField (if will be set).'''
        ...
    
    @options.setter
    def options(self, value: None):
        ...
    
    @property
    def selected(self) -> int:
        '''Gets/sets the value to determine property Selected for created ComboBoxField (if will be set).'''
        ...
    
    @selected.setter
    def selected(self, value: int):
        ...
    
    ...

class FormComboBoxFieldSetOptions(aspose.pdf.plugins.FormFieldSetOptions):
    '''Represents options for set properties in ComboBoxField by :class:`FormEditor` plugin.'''
    
    def __init__(self):
        ...
    
    @property
    def editable(self) -> bool:
        '''Gets/sets the value to determine property Editable for modified field (if will be set).'''
        ...
    
    @editable.setter
    def editable(self, value: bool):
        ...
    
    @property
    def options(self) -> None:
        '''Gets/sets the value to determine property Options for modified field (if will be set).'''
        ...
    
    @options.setter
    def options(self, value: None):
        ...
    
    @property
    def selected(self) -> int:
        '''Gets/sets the value to determine property Selected for modified field (if will be set).'''
        ...
    
    @selected.setter
    def selected(self, value: int):
        ...
    
    ...

class FormEditor:
    '''Represents FormEditor plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.FormEditorOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the FormEditor processing with the specified parameters.
        
        :param options: An options object containg instructions for the FormEditor.
        :returns: An ResultContainer object containg the result of the operation.
        
        :raises System.ArgumentException:'''
        ...
    
    ...

class FormEditorAddOptions(aspose.pdf.plugins.FormEditorOptions):
    '''Represents options for add Fields to document by :class:`FormEditor` plugin.'''
    
    def __init__(self, fields_create_options):
        ...
    
    ...

class FormEditorOptions(aspose.pdf.plugins.FormOptions):
    '''Represents options for :class:`FormEditor` plugin.'''
    
    ...

class FormEditorRemoveOptions(aspose.pdf.plugins.FormEditorOptions):
    '''Base class for option classes for remove fields in document by :class:`FormEditor` plugin.'''
    
    ...

class FormEditorSetOptions(aspose.pdf.plugins.FormEditorOptions):
    '''Represents options for set fields (not annotations) properties.'''
    
    ...

class FormExporter:
    '''Represents FormExporter plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.FormExporterOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the FormExporter processing with the specified parameters.
        
        :param options: An options object containg instructions for the FormExporter.
        :returns: An ResultContainer object containg the result of the operation.
        
        :raises System.ArgumentException:'''
        ...
    
    ...

class FormExporterOptions(aspose.pdf.plugins.FormOptions):
    '''Represents options for FormExporter plugin.'''
    
    ...

class FormExporterValuesToCsvOptions(aspose.pdf.plugins.FormExporterOptions):
    '''Represents options for export Value property(s) of specified field(s) (not annotations).'''
    
    ...

class FormFieldCreateOptions(aspose.pdf.plugins.FormFieldOptions):
    '''Represents options for creating Field.'''
    
    ...

class FormFieldOptions:
    '''Represents Field options. Base class for PdfFormFieldCreateOptions and PdfFormFillFieldOptions.'''
    
    @property
    def update_appearance_on_convert(self) -> bool:
        '''Gets/sets the value to determine whether created/modified field is update appearance on convert or not (if will be set).'''
        ...
    
    @update_appearance_on_convert.setter
    def update_appearance_on_convert(self, value: bool):
        ...
    
    @property
    def use_font_subset(self) -> bool:
        '''Gets/sets the value to determine whether created/modified field is use font subset or not (if will be set).'''
        ...
    
    @use_font_subset.setter
    def use_font_subset(self, value: bool):
        ...
    
    @property
    def flags(self) -> aspose.pdf.annotations.AnnotationFlags:
        '''Gets/sets the value to determine property Flags for created/modified field (if will be set).'''
        ...
    
    @flags.setter
    def flags(self, value: aspose.pdf.annotations.AnnotationFlags):
        ...
    
    @property
    def contents(self) -> str:
        '''Gets/sets the value to determine property Contents for created/modified field (if will be set).'''
        ...
    
    @contents.setter
    def contents(self, value: str):
        ...
    
    @property
    def name(self) -> str:
        '''Gets/sets the value to determine property Name for created/modified field (if will be set).'''
        ...
    
    @name.setter
    def name(self, value: str):
        ...
    
    @property
    def color(self) -> aspose.pdf.Color:
        '''Gets/sets the value to determine property Color for created/modified field (if will be set).'''
        ...
    
    @color.setter
    def color(self, value: aspose.pdf.Color):
        ...
    
    @property
    def text_horizontal_alignment(self) -> aspose.pdf.HorizontalAlignment:
        '''Gets/sets the value to determine property TextHorizontalAlignment for created/modified field (if will be set).'''
        ...
    
    @text_horizontal_alignment.setter
    def text_horizontal_alignment(self, value: aspose.pdf.HorizontalAlignment):
        ...
    
    @property
    def default_appearance(self) -> aspose.pdf.annotations.DefaultAppearance:
        '''Gets/sets the value to determine property DefaultAppearance for created/modified field (if will be set).'''
        ...
    
    @default_appearance.setter
    def default_appearance(self, value: aspose.pdf.annotations.DefaultAppearance):
        ...
    
    @property
    def read_only(self) -> bool:
        '''Gets/sets the value to determine whether created/modified field is read only or not (if will be set).'''
        ...
    
    @read_only.setter
    def read_only(self, value: bool):
        ...
    
    @property
    def required(self) -> bool:
        '''Gets/sets the value to determine whether created/modified field is required or not (if will be set).'''
        ...
    
    @required.setter
    def required(self, value: bool):
        ...
    
    @property
    def exportable(self) -> bool:
        '''Gets/sets the value to determine whether created/modified field is exportable or not (if will be set).'''
        ...
    
    @exportable.setter
    def exportable(self, value: bool):
        ...
    
    @property
    def partial_name(self) -> str:
        '''Gets/sets the value to determine property PartialName for created/modified field (if will be set).'''
        ...
    
    @partial_name.setter
    def partial_name(self, value: str):
        ...
    
    @property
    def alternate_name(self) -> str:
        '''Gets/sets the value to determine property AlternateName for created/modified field (if will be set).'''
        ...
    
    @alternate_name.setter
    def alternate_name(self, value: str):
        ...
    
    @property
    def mapping_name(self) -> str:
        '''Gets/sets the value to determine property MappingName for created/modified field (if will be set).'''
        ...
    
    @mapping_name.setter
    def mapping_name(self, value: str):
        ...
    
    @property
    def value(self) -> str:
        '''Gets/sets the value to determine property Value for created/modified field (if will be set).'''
        ...
    
    @value.setter
    def value(self, value: str):
        ...
    
    @property
    def is_shared_field(self) -> bool:
        '''Gets/sets the value to determine whether created/modified field is shared field or not (if will be set).'''
        ...
    
    @is_shared_field.setter
    def is_shared_field(self, value: bool):
        ...
    
    @property
    def fit_into_rectangle(self) -> bool:
        '''Gets/sets the value to determine whether created/modified field is fit into rectangle or not (if will be set).'''
        ...
    
    @fit_into_rectangle.setter
    def fit_into_rectangle(self, value: bool):
        ...
    
    @property
    def max_font_size(self) -> float:
        '''Gets/sets the value to determine property MaxFontSize for created/modified field (if will be set).'''
        ...
    
    @max_font_size.setter
    def max_font_size(self, value: float):
        ...
    
    @property
    def min_font_size(self) -> float:
        '''Gets/sets the value to determine property MinFontSize for created/modified field (if will be set).'''
        ...
    
    @min_font_size.setter
    def min_font_size(self, value: float):
        ...
    
    @property
    def highlighting(self) -> aspose.pdf.annotations.HighlightingMode:
        '''Gets/sets the value to determine property Highlighting for created/modified field (if will be set).'''
        ...
    
    @highlighting.setter
    def highlighting(self, value: aspose.pdf.annotations.HighlightingMode):
        ...
    
    ...

class FormFieldSetOptions(aspose.pdf.plugins.FormFieldOptions):
    '''Represents options for set properties in Field.'''
    
    def __init__(self):
        ...
    
    @property
    def rect(self) -> aspose.pdf.Rectangle:
        '''Rectangle that be setted to field(s).'''
        ...
    
    @rect.setter
    def rect(self, value: aspose.pdf.Rectangle):
        ...
    
    ...

class FormFlattenAllFieldsOptions(aspose.pdf.plugins.FormFlattenerOptions):
    '''Represents options for flatten all fields (not annotations) in document by :class:`FormFlattener` plugin.'''
    
    def __init__(self):
        ...
    
    ...

class FormFlattenSelectedFieldsOptions(aspose.pdf.plugins.FormFlattenerOptions):
    '''Represents options for flatten selected fields (not annotations) in document by :class:`FormFlattener` plugin.'''
    
    ...

class FormFlattener:
    '''Represents FormFlattener plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.FormFlattenerOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the FormFlattener processing with the specified parameters.
        
        :param options: An options object containg instructions for the FormFlattener.
        :returns: An ResultContainer object containg the result of the operation.
        
        :raises System.ArgumentException:'''
        ...
    
    ...

class FormFlattenerOptions(aspose.pdf.plugins.FormOptions):
    '''Base class for option classes for flatten fields (not annotations) in document by FormFlattener plugin.'''
    
    ...

class FormOptions:
    '''Represents options for a family Form....  plugins.'''
    
    def add_input(self, data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Adds new data source to the Form... plugins data collection.
        
        :param data_source: Data source to add.'''
        ...
    
    def add_output(self, save_data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Adds new data source to the Form... plugins data collection.
        
        :param save_data_source: Data source (file or stream) for saving operation results.
        :raises System.NotImplementedException:'''
        ...
    
    @property
    def inputs(self) -> None:
        '''Returns Form.... plugins data collection.'''
        ...
    
    @property
    def outputs(self) -> None:
        '''Gets collection of added targets for saving operation results.'''
        ...
    
    ...

class FormRemoveAllFieldsOptions(aspose.pdf.plugins.FormEditorRemoveOptions):
    '''Represents options for remove all fields in document by :class:`FormEditor` plugin.'''
    
    def __init__(self):
        ...
    
    ...

class FormRemoveSelectedFieldsOptions(aspose.pdf.plugins.FormEditorRemoveOptions):
    '''Represents options for remove selected fields in document by :class:`FormEditor` plugin.'''
    
    ...

class FormTextBoxFieldCreateOptions(aspose.pdf.plugins.FormFieldCreateOptions):
    '''Represents options for creating TextBoxField by :class:`FormEditor` plugin.'''
    
    def __init__(self, page_num: int, rect: aspose.pdf.Rectangle):
        '''Initializes a new instance of the :class:`FormTextBoxFieldCreateOptions` object, that containing parameters for created and added TextBoxField.
        
        :param page_num: Page number on which the added TextBoxField will be located.
        :param rect: Sets TextBoxField rectangle.'''
        ...
    
    @property
    def multiline(self) -> bool:
        '''Gets/sets the value to determine whether created TextBoxField is multiline or not (if will be set).'''
        ...
    
    @multiline.setter
    def multiline(self, value: bool):
        ...
    
    @property
    def spell_check(self) -> bool:
        '''Gets/sets the value to determine whether created TextBoxField is spellcheck or not (if will be set).'''
        ...
    
    @spell_check.setter
    def spell_check(self, value: bool):
        ...
    
    @property
    def force_combs(self) -> bool:
        '''Gets/sets the value to determine whether created TextBoxField is forcecombs or not (if will be set).'''
        ...
    
    @force_combs.setter
    def force_combs(self, value: bool):
        ...
    
    @property
    def max_len(self) -> int:
        '''Gets/sets the value to determine property MaxLen for created TextBoxField (if will be set).'''
        ...
    
    @max_len.setter
    def max_len(self, value: int):
        ...
    
    ...

class FormTextBoxFieldSetOptions(aspose.pdf.plugins.FormFieldSetOptions):
    '''Represents options for set properties in TextBoxField by :class:`FormEditor` plugin.'''
    
    def __init__(self):
        ...
    
    @property
    def multiline(self) -> bool:
        '''Gets/sets the value to determine property Multiline for modified field (if will be set).'''
        ...
    
    @multiline.setter
    def multiline(self, value: bool):
        ...
    
    @property
    def spell_check(self) -> bool:
        '''Gets/sets the value to determine property SpellCheck for modified field (if will be set).'''
        ...
    
    @spell_check.setter
    def spell_check(self, value: bool):
        ...
    
    @property
    def force_combs(self) -> bool:
        '''Gets/sets the value to determine property ForceCombs for modified field (if will be set).'''
        ...
    
    @force_combs.setter
    def force_combs(self, value: bool):
        ...
    
    @property
    def max_len(self) -> int:
        '''Gets/sets the value to determine property MaxLen for modified field (if will be set).'''
        ...
    
    @max_len.setter
    def max_len(self, value: int):
        ...
    
    ...

class HtmlToPdfOptions(aspose.pdf.plugins.PdfConverterOptions):
    '''Represents HTML to PDF converter options for :class:`PdfHtml` plugin.'''
    
    def __init__(self):
        ...
    
    @property
    def operation_name(self) -> str:
        '''Gets name of the operation.'''
        ...
    
    @property
    def is_render_to_single_page(self) -> bool:
        '''Gets or sets rendering all document to single page.'''
        ...
    
    @is_render_to_single_page.setter
    def is_render_to_single_page(self, value: bool):
        ...
    
    @property
    def base_path(self) -> str:
        '''The base path/url for the html file.'''
        ...
    
    @base_path.setter
    def base_path(self, value: str):
        ...
    
    @property
    def html_media_type(self) -> aspose.pdf.HtmlMediaType:
        '''Gets or sets possible media types used during rendering.'''
        ...
    
    @html_media_type.setter
    def html_media_type(self, value: aspose.pdf.HtmlMediaType):
        ...
    
    @property
    def page_layout_option(self) -> aspose.pdf.HtmlPageLayoutOption:
        '''Gets or sets layout option.'''
        ...
    
    @page_layout_option.setter
    def page_layout_option(self, value: aspose.pdf.HtmlPageLayoutOption):
        ...
    
    @property
    def page_info(self) -> aspose.pdf.PageInfo:
        '''Gets or sets document page info.'''
        ...
    
    @page_info.setter
    def page_info(self, value: aspose.pdf.PageInfo):
        ...
    
    ...

class IDataSource:
    '''General data source interface that defines common members that concrete data sources should implement.'''
    
    @property
    def data_type(self) -> None:
        '''Type of data source (file or stream).'''
        ...
    
    ...

class IOperationResult:
    '''General operation result interface that defines common methods that concrete plugin operation result should implement.'''
    
    def to_file(self) -> str:
        '''Tries to convert the result to the file.
        
        :returns: A string representing the path to the output file if the result is file; otherwise ``None``.'''
        ...
    
    def to_stream(self) -> Any:
        '''Tries to convert the result to the stream object.
        
        :returns: A stream object representing the output data if the result is stream; otherwise ``None``.'''
        ...
    
    @property
    def is_file(self) -> bool:
        '''Indicates whether the result is a path to an output file.
        
        :returns: ``True`` if the result is a file; otherwise ``False``.'''
        ...
    
    @property
    def is_stream(self) -> bool:
        '''Indicates whether the result is an output stream.
        
        :returns: ``True`` if the result is a stream object; otherwise ``False``.'''
        ...
    
    @property
    def is_string(self) -> bool:
        '''Indicates whether the result is a text string.
        
        :returns: ``True`` if the result is a string; otherwise ``False``.'''
        ...
    
    @property
    def data(self) -> object:
        '''Gets raw data.
        
        :returns: An ``object`` representing output data.'''
        ...
    
    ...

class IPlugin:
    '''General plugin interface that defines common methods that concrete plugin should implement.'''
    
    def process(self, options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Charges a plugin to process with defined options
        
        :param options: An options object containing instructions for the plugin
        :returns: An ResultContainer object containing the result of the processing'''
        ...
    
    ...

class IPluginOptions:
    '''General plugin option interface that defines common methods that concrete plugin option should implement.'''
    
    ...

class ImageExtractor:
    '''Represents ImageExtractor plugin.
    
    The :class:`ImageExtractor` object is used to extract text in PDF documents.'''
    
    def __init__(self):
        ...
    
    def process(self, pdf_extractor_options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        ...
    
    ...

class ImageExtractorOptions(aspose.pdf.plugins.PdfExtractorOptions):
    '''Represents images extraction options for the ImageExtractor plugin.
    
    It inherits functions to add data (files, streams) representing input PDF documents.'''
    
    def __init__(self):
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns name of the operation.'''
        ...
    
    ...

class Jpeg(aspose.pdf.plugins.PdfToImage):
    '''Represents Pdf to Jpeg plugin.'''
    
    def __init__(self):
        ...
    
    ...

class JpegOptions(aspose.pdf.plugins.PdfToImageOptions):
    '''Represents Pdf to Jpeg converter options for the :class:`Jpeg` plugin.'''
    
    def __init__(self):
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns name of the operation.'''
        ...
    
    @property
    def quality(self) -> int:
        '''Gets and sets Jpeg quality'''
        ...
    
    @quality.setter
    def quality(self, value: int):
        ...
    
    ...

class MergeOptions(aspose.pdf.plugins.OrganizerBaseOptions):
    '''Represents Merge options for :class:`Merger` plugin.'''
    
    def __init__(self):
        ...
    
    ...

class Merger:
    '''Represents :class:`Merger` plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the :class:`Merger` processing with the specified parameters.
        
        :param options: An options object containg instructions for the :class:`Merger`.
        :returns: An ResultContainer object containg the result of the operation.
        
        :raises System.InvalidOperationException:'''
        ...
    
    ...

class Message:
    
    def __init__(self):
        ...
    
    @property
    def content(self) -> str:
        ...
    
    @content.setter
    def content(self, value: str):
        ...
    
    @property
    def role(self) -> aspose.pdf.plugins.Role:
        ...
    
    @role.setter
    def role(self, value: aspose.pdf.plugins.Role):
        ...
    
    ...

class ObjectResult:
    '''Represents operation result in the form of string.'''
    
    def to_file(self) -> str:
        '''Tries to convert the result to a file.
        
        :returns: A string representing the path to the output file if the result is file; otherwise ``None``.'''
        ...
    
    def to_stream(self) -> Any:
        '''Tries to convert the result to a stream object.
        
        :returns: A stream object representing the output data if the result is stream; otherwise ``None``.'''
        ...
    
    @property
    def is_file(self) -> bool:
        '''Indicates whether the result is a path to an output file.
        
        :returns: ``True`` if the result is a file; otherwise ``False``.'''
        ...
    
    @property
    def is_stream(self) -> bool:
        '''Indicates whether the result is a path to an output file.
        
        :returns: ``True`` if the result is a stream object; otherwise ``False``.'''
        ...
    
    @property
    def is_string(self) -> bool:
        '''Indicates whether the result is a string.
        
        :returns: ``True`` if the result is a string; otherwise ``False``.'''
        ...
    
    @property
    def is_object(self) -> bool:
        '''Indicates whether the result is an object.
        
        :returns: ``True`` if the result is an object; otherwise ``False``.'''
        ...
    
    @property
    def data(self) -> object:
        '''Gets raw data.
        
        :returns: An ``object`` representing output data.'''
        ...
    
    @property
    def text(self) -> str:
        '''Returns string representation of the result.'''
        ...
    
    ...

class OptimizeOptions(aspose.pdf.plugins.OrganizerBaseOptions):
    '''Represents Optimize options for :class:`Optimizer` plugin.'''
    
    def __init__(self):
        ...
    
    ...

class Optimizer:
    '''Represents :class:`Optimizer` plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the :class:`Optimizer` processing with the specified parameters.
        
        :param options: An options object containg instructions for the :class:`Optimizer`.
        :returns: An ResultContainer object containg the result of the operation.
        
        :raises System.InvalidOperationException:'''
        ...
    
    ...

class OrganizerBaseOptions:
    '''Represents base options for plugins.'''
    
    def add_input(self, data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Adds new data source to the PdfOrganizer plugin data collection.
        
        :param data_source: Data source to add.'''
        ...
    
    def add_output(self, save_data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Adds new data source to the PdfOrganizer plugin data collection.
        
        :param save_data_source: Data source (file or stream) for saving operation results.
        :raises System.NotImplementedException:'''
        ...
    
    @property
    def inputs(self) -> None:
        '''Returns OrganizerOptions plugin data collection.'''
        ...
    
    @property
    def outputs(self) -> None:
        '''Gets collection of added targets for saving operation results.'''
        ...
    
    @property
    def close_input_streams(self) -> bool:
        '''Close input streams after operation completed.'''
        ...
    
    @close_input_streams.setter
    def close_input_streams(self, value: bool):
        ...
    
    @property
    def close_output_streams(self) -> bool:
        '''Close output streams after operation completed.'''
        ...
    
    @close_output_streams.setter
    def close_output_streams(self, value: bool):
        ...
    
    ...

class PdfAConvertOptions(aspose.pdf.plugins.PdfAOptionsBase):
    '''Represents options for converting PDF documents to PDF/A format with the :class:`PdfAConverter` plugin.'''
    
    def __init__(self):
        ...
    
    def add_output(self, data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Adds new result save target.
        
        :param data_source: Target (file or stream data source) for saving operation results.'''
        ...
    
    @property
    def outputs(self) -> None:
        '''Gets the collection of added targets (file or stream data sources) for saving operation results.'''
        ...
    
    ...

class PdfAConverter:
    '''Represents a plugin for handling the conversion of PDF documents in a PDF/A format and for validation of the PDF/A conformance.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Begins a PDF/A conversion or validation process with given options.
        
        :param options: An options object containing instructions for the plugin. Must be an instance of the :class:`PdfAConvertOptions`
                        or the :class:`PdfAValidateOptions` class.
        :returns: A :class:`ResultContainer` object containing the result of the processing.'''
        ...
    
    ...

class PdfAOptionsBase:
    '''Represents the base class for the :class:`PdfAConverter` plugin options.
    This class provides properties and methods for configuring the PDF/A conversion and validation process.'''
    
    def add_input(self, data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Adds new data source to the collection
        
        :param data_source:'''
        ...
    
    @property
    def inputs(self) -> None:
        '''Gets collection of data sources'''
        ...
    
    @property
    def pdf_a_version(self) -> aspose.pdf.plugins.PdfAStandardVersion:
        '''Gets or sets the version of the PDF/A standard to be used for validation or conversion.
        
        The PDF/A standard version is used to determine the compliance level for PDF/A validation and conversion.
        If the version is set to :attr:`PdfAStandardVersion.AUTO`, the system will automatically determine
        the appropriate PDF/A standard version for validation based on the document metadata.
        For the PDF/A conversion process the :attr:`PdfAStandardVersion.AUTO` defaults to the PDF/A-1b standard version.'''
        ...
    
    @pdf_a_version.setter
    def pdf_a_version(self, value: aspose.pdf.plugins.PdfAStandardVersion):
        ...
    
    @property
    def is_low_memory_mode(self) -> bool:
        '''Gets or sets a value indicating whether the low memory mode is enabled during the PDF/A conversion process.'''
        ...
    
    @is_low_memory_mode.setter
    def is_low_memory_mode(self, value: bool):
        ...
    
    @property
    def log_output_source(self) -> aspose.pdf.plugins.IDataSource:
        '''Gets or sets the data source for the log output.'''
        ...
    
    @log_output_source.setter
    def log_output_source(self, value: aspose.pdf.plugins.IDataSource):
        ...
    
    @property
    def error_action(self) -> aspose.pdf.ConvertErrorAction:
        '''Gets or sets the action to be taken for objects that cannot be converted.'''
        ...
    
    @error_action.setter
    def error_action(self, value: aspose.pdf.ConvertErrorAction):
        ...
    
    @property
    def soft_mask_action(self) -> aspose.pdf.ConvertSoftMaskAction:
        '''Gets or sets the action to be taken during the conversion of images with soft masks.'''
        ...
    
    @soft_mask_action.setter
    def soft_mask_action(self, value: aspose.pdf.ConvertSoftMaskAction):
        ...
    
    @property
    def non_specification_flags(self) -> aspose.pdf.PdfANonSpecificationFlags:
        '''Gets the flags that control the PDF/A conversion for cases when the source PDF document doesn't
        correspond to the PDF specification.'''
        ...
    
    @property
    def symbolic_font_encoding_strategy(self) -> aspose.pdf.PdfASymbolicFontEncodingStrategy:
        '''Gets or sets the strategy for encoding symbolic fonts when converting to PDF/A format.
        
        This property allows you to control what CMap subtable would be copied into the result document in cases when the original
        TrueType symbolic font in the source document contains multiple CMap subtables.'''
        ...
    
    @symbolic_font_encoding_strategy.setter
    def symbolic_font_encoding_strategy(self, value: aspose.pdf.PdfASymbolicFontEncodingStrategy):
        ...
    
    @property
    def align_text(self) -> bool:
        '''Gets or sets a value indicating whether additional means are necessary to preserve text alignment
        during the PDF/A conversion process.
        
        When set to true, the conversion process will attempt to restore the original text segment bounds.
        For the most of the documents there is no need to change this property from the default false value,
        as the text alignment doesn't change during the default conversion process.'''
        ...
    
    @align_text.setter
    def align_text(self, value: bool):
        ...
    
    @property
    def pua_symbols_processing_strategy(self) -> None:
        '''Gets or sets the strategy for processing Private Use Area (PUA) symbols in the PDF document.'''
        ...
    
    @pua_symbols_processing_strategy.setter
    def pua_symbols_processing_strategy(self, value: None):
        ...
    
    @property
    def optimize_file_size(self) -> bool:
        '''Gets or sets a value indicating whether to try to reduce the file size during the PDF/A conversion process.
        
        When set to true, the conversion process will attempt to minimize the resulting file size.
        This might affect the conversion process performance.'''
        ...
    
    @optimize_file_size.setter
    def optimize_file_size(self, value: bool):
        ...
    
    @property
    def exclude_fonts_strategy(self) -> None:
        '''Gets or sets the strategy for removing fonts to minimize the output file size during the PDF/A conversion process.
        
        This property allows you to control how fonts are handled during the conversion process.
        You can choose to remove duplicated fonts, remove similar fonts with different widths, or subset fonts.'''
        ...
    
    @exclude_fonts_strategy.setter
    def exclude_fonts_strategy(self, value: None):
        ...
    
    @property
    def font_embedding_options(self) -> aspose.pdf.pdfaoptionclasses.FontEmbeddingOptions:
        '''Gets the options to process fonts that cannot be embedded into the document.
        
        The PDF/A standard requires that all fonts must be embedded into the document.
        This property provides options for handling cases when it's not possible to embed some fonts because they are absent on the destination PC.'''
        ...
    
    @property
    def unicode_processing_rules(self) -> aspose.pdf.pdfaoptionclasses.ToUnicodeProcessingRules:
        '''Gets or sets the rules for processing ToUnicode CMap tables and not linked to Unicode symbols during the PDF/A conversion process.'''
        ...
    
    @unicode_processing_rules.setter
    def unicode_processing_rules(self, value: aspose.pdf.pdfaoptionclasses.ToUnicodeProcessingRules):
        ...
    
    @property
    def icc_profile_file_name(self) -> str:
        '''Gets or sets the filename of the ICC (International Color Consortium) profile to be used for the PDF/A conversion in place of
        the default one.'''
        ...
    
    @icc_profile_file_name.setter
    def icc_profile_file_name(self, value: str):
        ...
    
    ...

class PdfAValidateOptions(aspose.pdf.plugins.PdfAOptionsBase):
    '''Represents options for validating PDF/A compliance of PDF documents with the :class:`PdfAConverter` plugin.'''
    
    def __init__(self):
        ...
    
    ...

class PdfAValidationResult:
    '''Represents the result of a PDF/A validation process.'''
    
    @property
    def DATA_SOURCE(self) -> aspose.pdf.plugins.IDataSource:
        '''Gets the data source that was validated.'''
        ...
    
    @property
    def STANDARD_VERSION(self) -> aspose.pdf.plugins.PdfAStandardVersion:
        '''Gets the PDF/A standard version used for validation.'''
        ...
    
    @property
    def IS_VALID(self) -> bool:
        '''Gets a value indicating whether the validation was successful.'''
        ...
    
    ...

class PdfChatGpt:
    
    def __init__(self):
        ...
    
    ...

class PdfChatGptOptions:
    
    def __init__(self):
        ...
    
    def add_input(self, data_source: aspose.pdf.plugins.IDataSource) -> None:
        ...
    
    def add_output(self, save_data_source: aspose.pdf.plugins.IDataSource) -> None:
        ...
    
    @property
    def inputs(self) -> None:
        ...
    
    @property
    def outputs(self) -> None:
        ...
    
    ...

class PdfChatGptRequestOptions(aspose.pdf.plugins.PdfChatGptOptions):
    
    @overload
    def __init__(self):
        ...
    
    @overload
    def __init__(self, api_key: str, model: str, api_url: str, query: str):
        ...
    
    @property
    def api_key(self) -> str:
        ...
    
    @api_key.setter
    def api_key(self, value: str):
        ...
    
    @property
    def api_url(self) -> str:
        ...
    
    @api_url.setter
    def api_url(self, value: str):
        ...
    
    @property
    def query(self) -> str:
        ...
    
    @query.setter
    def query(self, value: str):
        ...
    
    @property
    def messages(self) -> None:
        ...
    
    @messages.setter
    def messages(self, value: None):
        ...
    
    @property
    def max_tokens(self) -> int:
        ...
    
    @max_tokens.setter
    def max_tokens(self, value: int):
        ...
    
    @property
    def model(self) -> str:
        ...
    
    @model.setter
    def model(self, value: str):
        ...
    
    @property
    def number_of_choices(self) -> int:
        ...
    
    @number_of_choices.setter
    def number_of_choices(self, value: int):
        ...
    
    @property
    def temperature(self) -> float:
        ...
    
    @temperature.setter
    def temperature(self, value: float):
        ...
    
    ...

class PdfConverterOptions:
    '''Represents options for Pdf converter plugins.'''
    
    def add_input(self, data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Adds new data source to the PdfConverter plugin data collection.
        
        :param data_source: Data source to add.'''
        ...
    
    def add_output(self, save_data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Adds new data source to the PdfToXLSXConverterOptions plugin data collection.
        
        :param save_data_source: Data source (file or stream) for saving operation results.
        :raises System.NotImplementedException:'''
        ...
    
    @property
    def inputs(self) -> None:
        '''Returns PdfConverterOptions plugin data collection.'''
        ...
    
    @property
    def outputs(self) -> None:
        '''Gets collection of added targets for saving operation results.'''
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns operation name.'''
        ...
    
    ...

class PdfDoc:
    '''Represents :class:`PdfDoc` plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the :class:`PdfDoc` processing with the specified parameters.
        
        :param options: An options object containing instructions for the :class:`PdfDoc`.
        :returns: An :class:`ResultContainer` object containing the result of the operation.'''
        ...
    
    ...

class PdfExtractor:
    '''Represents base functionality to extract text, images, and other types of content that may occur on the pages of PDF documents.
    
    The :class:`TextExtractor` object is used to extract text, or :class:`ImageExtractor` to extract images.'''
    
    def process(self, pdf_extractor_options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts PdfExtractor processing with the specified parameters.
        
        :param pdf_extractor_options: An options object containing instructions for the PdfExtractor.
        :returns: A ResultContainer object containing the result of the extraction.'''
        ...
    
    ...

class PdfExtractorOptions:
    '''Represents options for the TextExtractor and ImageExtractor plugins.
    
    The :class:`PdfExtractorOptions` contains base functions to add data (files, streams) representing input PDF documents.
    Please create :class:`TextExtractorOptions` or ImageExtractorOptions instead of this.'''
    
    def add_input(self, data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Adds new data source to the PdfExtractor plugin data collection.
        
        :param data_source: Data source to add.'''
        ...
    
    @property
    def inputs(self) -> None:
        '''Returns PdfExtractor plugin data collection.'''
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns operation name'''
        ...
    
    ...

class PdfGeneratorOptions:
    '''Represents options for Generator plugins.'''
    
    def add_input(self, data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Adds new data source to the PdfGenerator plugin data collection.
        
        :param data_source: Data source to add.'''
        ...
    
    def add_output(self, save_data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Adds new data source to the PdfGenerator plugin data collection.
        
        :param save_data_source: Data source (file or stream) for saving operation results.'''
        ...
    
    @property
    def inputs(self) -> None:
        '''Returns PdfGenerator plugin data collection.'''
        ...
    
    @property
    def outputs(self) -> None:
        '''Gets collection of added targets for saving operation results.'''
        ...
    
    ...

class PdfHtml:
    '''Represents :class:`PdfHtml` plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the :class:`PdfHtml` processing with the specified parameters.
        
        :param options: An options object containing instructions for the :class:`PdfHtml`.
        :returns: An :class:`ResultContainer` object containing the result of the operation.'''
        ...
    
    ...

class PdfToDocOptions(aspose.pdf.plugins.PdfConverterOptions):
    '''Represents PDF to DOC converter options for :class:`PdfDoc` plugin.'''
    
    @overload
    def __init__(self):
        '''Initializes new instance of the :class:`PdfToDocOptions` object with default options.'''
        ...
    
    @overload
    def __init__(self, format, mode: aspose.pdf.plugins.ConversionMode):
        '''Initializes a new instance of the :class:`PdfToDocOptions` object for the specified format and mode.
        
        :param format: Save format of the :attr:`PdfToDocOptions.save_format` output document.
        :param mode: Conversion mode of the :attr:`PdfToDocOptions.conversion_mode` output document.'''
        ...
    
    @property
    def operation_name(self) -> str:
        '''Gets name of the operation.'''
        ...
    
    @property
    def save_format(self) -> None:
        '''Save format of the output document.'''
        ...
    
    @save_format.setter
    def save_format(self, value: None):
        ...
    
    @property
    def conversion_mode(self) -> aspose.pdf.plugins.ConversionMode:
        '''Allows to control how a PDF document is converted into a word processing document.
        
        Use the :attr:`ConversionMode.TEXT_BOX` mode when the resulting document is not going
        to be heavily edited further. Textboxes are easy to modify when there is not a lot to do.
        
        Use the :attr:`ConversionMode.FLOW` mode when the output document needs further editing.
        Paragraphs and text lines in the flow mode allow easy modification of text, but unsupported
        formatting objects will look worse than in the :attr:`ConversionMode.TEXT_BOX` mode.'''
        ...
    
    @conversion_mode.setter
    def conversion_mode(self, value: aspose.pdf.plugins.ConversionMode):
        ...
    
    ...

class PdfToHtmlOptions(aspose.pdf.plugins.PdfConverterOptions):
    '''Represents PDF to HTML converter options for :class:`PdfHtml` plugin.'''
    
    @overload
    def __init__(self):
        '''Initializes new instance of the :class:`PdfToHtmlOptions` object with default options.'''
        ...
    
    @overload
    def __init__(self, output_data_type):
        '''Initializes a new instance of the :class:`PdfToHtmlOptions` object for the specified output data type.
        
        :param output_data_type: Output data type.'''
        ...
    
    @property
    def operation_name(self) -> str:
        '''Gets name of the operation.'''
        ...
    
    @property
    def output_data_type(self) -> None:
        '''Gets output data type.'''
        ...
    
    ...

class PdfToImage:
    '''Represents PDF to image plugin.
    
    The :class:`PdfToImage` class is used to convert PDF document to images'''
    
    def process(self, pdf_image_options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts  processing with the specified parameters.
        
        :param pdf_image_options: An options object containing instructions for the PdfImage.
        :returns: A ResultContainer object containing the result of the conversion.'''
        ...
    
    ...

class PdfToImageOptions:
    '''Represents options for the :class:`PdfToImage` plugin.
    
    The PdfImageOptions class contains base functions to add data (files, streams) representing input PDF documents.'''
    
    def add_input(self, data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Adds new data source to the :class:`PdfToImage` plugin data collection.
        
        :param data_source: Data source to add.'''
        ...
    
    def add_output(self, save_data_source: aspose.pdf.plugins.IDataSource) -> None:
        '''Sets new save data source. Can only be a . If you want save images into memory streams, pass null as parameter.
        
        :param save_data_source: Save data source.'''
        ...
    
    @property
    def inputs(self) -> None:
        '''Returns :class:`PdfToImage` plugin data collection.'''
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns operation name.'''
        ...
    
    @property
    def outputs(self) -> None:
        ...
    
    @property
    def conversion_mode(self) -> None:
        '''Gets image conversion mode.'''
        ...
    
    @property
    def page_list(self) -> None:
        '''Gets or sets a list of pages for the process.'''
        ...
    
    @page_list.setter
    def page_list(self, value: None):
        ...
    
    @property
    def output_resolution(self) -> int:
        '''Gets or sets the resolution value of the resulting images.'''
        ...
    
    @output_resolution.setter
    def output_resolution(self, value: int):
        ...
    
    ...

class PdfToXlsOptions(aspose.pdf.plugins.PdfConverterOptions):
    '''Represents PDF to XLSX converter options for :class:`PdfXls` plugin.'''
    
    def __init__(self):
        ...
    
    @property
    def operation_name(self) -> str:
        '''Gets name of the operation.'''
        ...
    
    @property
    def minimize_the_number_of_worksheets(self) -> bool:
        '''Set true if you need to minimize the number of worksheets in resultant workbook.
        Default value is false; it means save of each PDF page as separated worksheet.'''
        ...
    
    @minimize_the_number_of_worksheets.setter
    def minimize_the_number_of_worksheets(self, value: bool):
        ...
    
    @property
    def insert_blank_column_at_first(self) -> bool:
        '''Set true if you need inserting of blank column as the first column of worksheet.
        Default value is false; it means that blank column will not be inserted.'''
        ...
    
    @insert_blank_column_at_first.setter
    def insert_blank_column_at_first(self, value: bool):
        ...
    
    @property
    def format(self) -> None:
        '''Output format.'''
        ...
    
    @format.setter
    def format(self, value: None):
        ...
    
    ...

class PdfXls:
    '''Represents :class:`PdfXls` plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the PdfToExcel processing with the specified parameters.
        
        :param options: An options object containing instructions for the :class:`PdfXls`.
        :returns: An :class:`ResultContainer` object containing the result of the operation.'''
        ...
    
    ...

class Png(aspose.pdf.plugins.PdfToImage):
    '''Represents Pdf to Png plugin.'''
    
    def __init__(self):
        ...
    
    ...

class PngOptions(aspose.pdf.plugins.PdfToImageOptions):
    '''Represents Pdf to Png converter options for the :class:`Png` plugin.'''
    
    def __init__(self):
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns name of the operation.'''
        ...
    
    ...

class ResizeOptions(aspose.pdf.plugins.OrganizerBaseOptions):
    '''Represents Resize options for :class:`Optimizer` plugin.'''
    
    def __init__(self):
        ...
    
    @property
    def page_size(self) -> aspose.pdf.PageSize:
        '''Gets or sets new page size.'''
        ...
    
    @page_size.setter
    def page_size(self, value: aspose.pdf.PageSize):
        ...
    
    ...

class ResultContainer:
    '''Represents container that contains the result collection of processing the plugin.'''
    
    @property
    def result_collection(self) -> None:
        '''Gets collection of the operation results'''
        ...
    
    ...

class RotateOptions(aspose.pdf.plugins.OrganizerBaseOptions):
    '''Represents Rotate options for :class:`Optimizer` plugin.'''
    
    def __init__(self):
        ...
    
    @property
    def rotation(self) -> aspose.pdf.Rotation:
        '''Gets or sets new pages rotation.'''
        ...
    
    @rotation.setter
    def rotation(self, value: aspose.pdf.Rotation):
        ...
    
    ...

class Security:
    '''Represents :class:`Security` plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the :class:`Security` processing with the specified parameters.
        
        :param options: An options object containg instructions for the :class:`Security`.
        :returns: A ResultContainer object containg the result of the operation.
        
        :raises System.InvalidOperationException:'''
        ...
    
    ...

class SignOptions(aspose.pdf.plugins.OrganizerBaseOptions):
    '''Represents Sign Options for :class:`Signature` plugin.'''
    
    @overload
    def __init__(self, pfx: str, password: str):
        '''Initializes new instance of the :class:`SignOptions` object with default options.
        
        :param pfx: The path to the pfx file.
        :param password: The password to the pfx file.'''
        ...
    
    @overload
    def __init__(self, pfx: Any, password: str):
        '''Initializes new instance of the :class:`SignOptions` object with default options.
        
        :param pfx: The stream with the pfx file.
        :param password: The password to the pfx file.'''
        ...
    
    @property
    def page_number(self) -> int:
        '''The page number on which signature is made.'''
        ...
    
    @page_number.setter
    def page_number(self, value: int):
        ...
    
    @property
    def visible(self) -> bool:
        '''The visiblity of signature.'''
        ...
    
    @visible.setter
    def visible(self, value: bool):
        ...
    
    @property
    def rectangle(self) -> aspose.pdf.Rectangle:
        '''The rect of signature.'''
        ...
    
    @rectangle.setter
    def rectangle(self, value: aspose.pdf.Rectangle):
        ...
    
    @property
    def reason(self) -> str:
        '''The reason of signature.'''
        ...
    
    @reason.setter
    def reason(self, value: str):
        ...
    
    @property
    def contact(self) -> str:
        '''The contact of signature.'''
        ...
    
    @contact.setter
    def contact(self, value: str):
        ...
    
    @property
    def location(self) -> str:
        '''The location of signature.'''
        ...
    
    @location.setter
    def location(self, value: str):
        ...
    
    @property
    def name(self) -> str:
        '''The name of existing signature field.
        Null to create a new field.'''
        ...
    
    @name.setter
    def name(self, value: str):
        ...
    
    ...

class Signature:
    '''Represents :class:`Signature` plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the :class:`Signature` processing with the specified parameters.
        
        :param options: An options object containg instructions for the :class:`Signature`.
        :returns: An ResultContainer object containg the result of the operation.
        
        :raises System.InvalidOperationException:'''
        ...
    
    ...

class SplitOptions(aspose.pdf.plugins.OrganizerBaseOptions):
    '''Represents Split options for :class:`Splitter` plugin.'''
    
    def __init__(self):
        ...
    
    ...

class Splitter:
    '''Represents :class:`Splitter` plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the :class:`Splitter` processing with the specified parameters.
        
        :param options: An options object containg instructions for the :class:`Splitter`.
        :returns: An ResultContainer object containg the result of the operation.
        
        :raises System.InvalidOperationException:'''
        ...
    
    ...

class StreamDataSource:
    '''Represents stream data source for load and save operations of a plugin.'''
    
    def __init__(self, data: Any):
        '''Initializes new stream data source with the specified stream object.
        
        :param data: Stream object'''
        ...
    
    @property
    def data_type(self) -> None:
        '''Type of data source (stream).'''
        ...
    
    @property
    def data(self) -> Any:
        '''Gets the stream object of the current data source.'''
        ...
    
    ...

class StreamResult:
    '''Represents operation result in the form of Stream.'''
    
    def to_file(self) -> str:
        '''Tries to convert the result to a file.
        
        :returns: A string representing the path to the output file if the result is file; otherwise ``None``.'''
        ...
    
    def to_stream(self) -> Any:
        '''Tries to convert the result to a stream object.
        
        :returns: A stream object representing the output data if the result is stream; otherwise ``None``.'''
        ...
    
    @property
    def is_file(self) -> bool:
        '''Indicates whether the result is a path to an output file.
        
        :returns: ``True`` if the result is a file; otherwise ``False``.'''
        ...
    
    @property
    def is_stream(self) -> bool:
        '''Indicates whether the result is a path to an output file.
        
        :returns: ``True`` if the result is a stream object; otherwise ``False``.'''
        ...
    
    @property
    def is_string(self) -> bool:
        '''Indicates whether the result is a string.
        
        :returns: ``True`` if the result is a string; otherwise ``False``.'''
        ...
    
    @property
    def data(self) -> object:
        '''Gets raw data.
        
        :returns: An ``object`` representing output data.'''
        ...
    
    ...

class StringResult:
    '''Represents operation result in the form of string.'''
    
    def to_file(self) -> str:
        '''Tries to convert the result to a file.
        
        :returns: A string representing the path to the output file if the result is file; otherwise ``None``.'''
        ...
    
    def to_stream(self) -> Any:
        '''Tries to convert the result to a stream object.
        
        :returns: A stream object representing the output data if the result is stream; otherwise ``None``.'''
        ...
    
    @property
    def is_file(self) -> bool:
        '''Indicates whether the result is a path to an output file.
        
        :returns: ``True`` if the result is a file; otherwise ``False``.'''
        ...
    
    @property
    def is_stream(self) -> bool:
        '''Indicates whether the result is a path to an output file.
        
        :returns: ``True`` if the result is a stream object; otherwise ``False``.'''
        ...
    
    @property
    def is_string(self) -> bool:
        '''Indicates whether the result is a string.
        
        :returns: ``True`` if the result is a string; otherwise ``False``.'''
        ...
    
    @property
    def data(self) -> object:
        '''Gets raw data.
        
        :returns: An ``object`` representing output data.'''
        ...
    
    @property
    def text(self) -> str:
        '''Returns string representation of the result.'''
        ...
    
    ...

class TableBuilder:
    '''Class represents builder for table in pdf page.'''
    
    def add_row(self) -> aspose.pdf.plugins.TableRowBuilder:
        '''Add new row to table.
        
        :returns: Instance of current :class:`TableRowBuilder`.'''
        ...
    
    def add_table(self) -> aspose.pdf.plugins.TableBuilder:
        '''Add new table to document.
        
        :returns: Instance of current :class:`TableBuilder`.'''
        ...
    
    def insert_page_after(self, page: int) -> aspose.pdf.plugins.TableOptions:
        '''Insert page after specified page.
        
        :param page: Page number to insert table after.
        :returns: Instance of current :class:`TableOptions`.'''
        ...
    
    def insert_page_before(self, page: int) -> aspose.pdf.plugins.TableOptions:
        '''Insert page before specified page.
        
        :param page: Page number to insert table after.
        :returns: Instance of current :class:`TableOptions`.'''
        ...
    
    ...

class TableCellBuilder(aspose.pdf.plugins.TableRowBuilder):
    '''Class represents builder for table cell.'''
    
    def add_cell(self) -> aspose.pdf.plugins.TableCellBuilder:
        '''Add cell to table.
        
        :returns: Instance of current :class:`TableCellBuilder`.'''
        ...
    
    def add_paragraph(self, paragraph: list[aspose.pdf.BaseParagraph]) -> aspose.pdf.plugins.TableCellBuilder:
        '''Add paragraphs to table cell.
        
        :param paragraph:
        :returns: Instance of current :class:`TableCellBuilder`.'''
        ...
    
    ...

class TableGenerator:
    '''Represents Aspose.PDF TableGenerator plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the PdfGenerator processing with the specified parameters.
        
        :param options: An options object contains instructions for the PdfGenerator.
        :returns: An ResultContainer object contains the result of the operation.
        
        :raises System.NotSupportedException:'''
        ...
    
    ...

class TableOptions(aspose.pdf.plugins.PdfGeneratorOptions):
    '''Represents options for add table to document by :class:`TableGenerator` plugin.'''
    
    def __init__(self):
        ...
    
    def insert_page_after(self, page: int) -> aspose.pdf.plugins.TableOptions:
        '''Insert page after specified page.
        
        :param page: Page number to insert table after.
        :returns: Instance of current :class:`TableOptions`.'''
        ...
    
    def insert_page_before(self, page: int) -> aspose.pdf.plugins.TableOptions:
        '''Insert page before specified page.
        
        :param page: Page number to insert table after.
        :returns: Instance of current :class:`TableOptions`.'''
        ...
    
    def add_table(self) -> aspose.pdf.plugins.TableBuilder:
        '''Adding table to document.
        
        :returns: New instance of :class:`TableBuilder`.'''
        ...
    
    @staticmethod
    def create(self) -> aspose.pdf.plugins.TableOptions:
        '''Create instance of :class:`TableOptions`.
        
        :returns: New instance of :class:`TableOptions`.'''
        ...
    
    ...

class TableRowBuilder(aspose.pdf.plugins.TableBuilder):
    '''Class represents builder for table row.'''
    
    def add_row(self) -> aspose.pdf.plugins.TableRowBuilder:
        '''Overriding AddRow.
        
        :returns: Instance of current :class:`TableRowBuilder`.'''
        ...
    
    def add_cell(self) -> aspose.pdf.plugins.TableCellBuilder:
        '''Add cell to table row.
        
        :returns: Instance of created :class:`TableCellBuilder`.'''
        ...
    
    ...

class TextExtractor:
    '''Represents TextExtractor plugin.
    
    The :class:`TextExtractor` object is used to extract text in PDF documents.'''
    
    def __init__(self):
        ...
    
    def process(self, pdf_extractor_options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        ...
    
    ...

class TextExtractorOptions(aspose.pdf.plugins.PdfExtractorOptions):
    '''Represents text extraction options for the TextExtractor plugin.
    
    The :class:`TextExtractorOptions` object is used to set Aspose.Pdf.Plugins.TextExtractorOptions.TextFormattingMode and another options for the text extraction operation.
    Also, it inherits functions to add data (files, streams) representing input PDF documents.'''
    
    @overload
    def __init__(self, formatting_mode):
        '''Initializes a new instance of the :class:`TextExtractorOptions` object for the specified text formatting mode.
        
        :param formatting_mode: Text formatting mode value.'''
        ...
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the :class:`TextExtractorOptions` object with 'Raw' (default) text formatting mode.'''
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns name of the operation.'''
        ...
    
    @property
    def formatting_mode(self) -> None:
        '''Gets formatting mode.'''
        ...
    
    ...

class Tiff(aspose.pdf.plugins.PdfToImage):
    '''Represents Pdf to Tiff plugin.'''
    
    def __init__(self):
        ...
    
    ...

class TiffOptions(aspose.pdf.plugins.PdfToImageOptions):
    '''Represents Pdf to Tiff converter options for the :class:`Tiff` plugin.'''
    
    def __init__(self):
        ...
    
    @property
    def operation_name(self) -> str:
        '''Returns name of the operation.'''
        ...
    
    @property
    def save_as_multi_page_tiff(self) -> bool:
        '''Gets and sets flag that allows to save all pages in one multi-page tiff.'''
        ...
    
    @save_as_multi_page_tiff.setter
    def save_as_multi_page_tiff(self, value: bool):
        ...
    
    @property
    def compression(self) -> aspose.pdf.devices.CompressionType:
        '''Gets or sets the type of the compression.
        
        Default value is CompressionType.LZW'''
        ...
    
    @compression.setter
    def compression(self, value: aspose.pdf.devices.CompressionType):
        ...
    
    @property
    def depth(self) -> aspose.pdf.devices.ColorDepth:
        '''Gets or sets the color depth.
        
        Default value is ColorDepth.Default'''
        ...
    
    @depth.setter
    def depth(self, value: aspose.pdf.devices.ColorDepth):
        ...
    
    @property
    def brightness(self) -> float:
        '''Get or sets a value boundary of the transformation of colors in white and black.
        This parameter can be applied with EncoderValue.CompressionCCITT4, EncoderValue.CompressionCCITT3, EncoderValue.CompressionRle or ColorDepth.Format1bpp == 1'''
        ...
    
    @brightness.setter
    def brightness(self, value: float):
        ...
    
    @property
    def coordinate_type(self) -> aspose.pdf.PageCoordinateType:
        '''Get or sets the page coordinate type (Media/Crop boxes). CropBox value is used by default.'''
        ...
    
    @coordinate_type.setter
    def coordinate_type(self, value: aspose.pdf.PageCoordinateType):
        ...
    
    @property
    def skip_blank_pages(self) -> bool:
        '''Gets or sets a value indicating whether to skip blank pages.
        
        Default value is false'''
        ...
    
    @skip_blank_pages.setter
    def skip_blank_pages(self, value: bool):
        ...
    
    @property
    def shape(self) -> aspose.pdf.devices.ShapeType:
        '''Gets or sets the type of the shape.
        
        Default value is ShapeType.None'''
        ...
    
    @shape.setter
    def shape(self, value: aspose.pdf.devices.ShapeType):
        ...
    
    ...

class TocGenerator:
    '''Represents Aspose.PDF TocGenerator plugin.'''
    
    def __init__(self):
        ...
    
    def process(self, options: aspose.pdf.plugins.IPluginOptions) -> aspose.pdf.plugins.ResultContainer:
        '''Starts the PdfGenerator processing with the specified parameters.
        
        :param options: An options object contains instructions for the PdfGenerator.
        :returns: An ResultContainer object contains the result of the operation.
        
        :raises System.NotSupportedException:'''
        ...
    
    ...

class TocOptions(aspose.pdf.plugins.PdfGeneratorOptions):
    '''Represents options for add table of contents to document by :class:`TocGenerator` plugin.'''
    
    def __init__(self):
        ...
    
    ...

class Usage:
    
    def __init__(self):
        ...
    
    @property
    def prompt_tokens(self) -> int:
        ...
    
    @prompt_tokens.setter
    def prompt_tokens(self, value: int):
        ...
    
    @property
    def completion_tokens(self) -> int:
        ...
    
    @completion_tokens.setter
    def completion_tokens(self, value: int):
        ...
    
    @property
    def total_tokens(self) -> int:
        ...
    
    @total_tokens.setter
    def total_tokens(self, value: int):
        ...
    
    ...

class ConversionMode:
    '''Defines conversion mode of the output document.'''
    
    TEXT_BOX: ConversionMode
    FLOW: ConversionMode
    ENHANCED_FLOW: ConversionMode

class DataType:
    '''Represents possible types of data for plugin processing.'''
    
    FILE: DataType
    STREAM: DataType

class PdfAStandardVersion:
    '''Specifies the PDF/A standard version for a PDF document.'''
    
    AUTO: PdfAStandardVersion
    PDF_A_1A: PdfAStandardVersion
    PDF_A_1B: PdfAStandardVersion
    PDF_A_2A: PdfAStandardVersion
    PDF_A_2B: PdfAStandardVersion
    PDF_A_2U: PdfAStandardVersion
    PDF_A_3A: PdfAStandardVersion
    PDF_A_3B: PdfAStandardVersion
    PDF_A_3U: PdfAStandardVersion

class Role:
    
    USER: Role
    SYSTEM: Role
    ASSISTANT: Role

class SaveFormat:
    '''Allows to specify .doc or .docx file format.'''
    
    DOC: SaveFormat
    DOC_X: SaveFormat

