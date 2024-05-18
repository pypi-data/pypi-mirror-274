from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import ClassVar, List, Optional

import geopandas as gpd
from pydantic import BaseModel, BaseSettings, Field
from typing_extensions import List, Literal, Union


class AccessDBInputs(BaseModel):
    class Config:
        extra = "forbid"

    label: ClassVar[str] = "digitale_standaard"
    description: ClassVar[str] = "Draai veg2hab o.b.v. de digitale standaard"
    shapefile: str = Field(
        description="Locatie van de vegetatiekartering",
    )
    elmid_col: str = Field(
        description="De kolomnaam van de ElementID in de Shapefile; deze wordt gematched aan de Element tabel in de AccessDB",
    )
    access_mdb_path: Path = Field(
        description="Locatie van de .mdb file van de digitale standaard",
    )
    datum_col: Optional[str] = Field(
        default=None,
        description="Datum kolom (optioneel), deze wordt onveranderd aan de output meegegeven",
    )
    opmerking_col: Optional[str] = Field(
        default=None,
        description="Opmerking kolom (optioneel), deze wordt onveranderd aan de output meegegeven",
    )
    output: Optional[Path] = Field(
        default=None,
        description="Output bestand (optioneel), indien niet gegeven wordt er een bestandsnaam gegenereerd",
    )


class ShapefileInputs(BaseModel):
    class Config:
        extra = "forbid"

    label: ClassVar[str] = "vector_bestand"
    description: ClassVar[str] = "Draai veg2hab o.b.v. een vector bestand"
    shapefile: str = Field(
        description="Locatie van de vegetatiekartering",
    )
    elmid_col: Optional[str] = Field(
        description="De kolomnaam van de ElementID in de Shapefile; uniek per vlak",
    )
    vegtype_col_format: Literal["single", "multi"] = Field(
        description='"single" als complexen in 1 kolom zitten of "multi" als er meerdere kolommen zijn',
    )
    sbb_of_vvn: Literal["SBB", "VvN", "beide"] = Field(
        description='"VvN" als VvN de voorname vertaling is vanuit het lokale type, "SBB" voor SBB en "beide" als beide er zijn.'
    )
    sbb_col: List[str] = Field(
        default_factory=list,
        description="SBB kolom(men) (verplicht wanneer het voorname type 'SBB' of 'beide' is)",
    )
    vvn_col: List[str] = Field(
        default_factory=list,
        description="VvN kolom(men) (verplicht wanneer het voorname type 'VvN' of 'beide' is)",
    )
    perc_col: List[str] = Field(
        default_factory=list,
        description="Percentage kolom(men) (optioneel)",
    )
    lok_vegtypen_col: List[str] = Field(
        default_factory=list,
        description="Lokale vegetatietypen kolom(men) (optioneel)",
    )
    split_char: Optional[str] = Field(
        default="+",
        description='Karakter waarop de complexe vegetatietypen gesplitst moeten worden (voor complexen (bv "16aa2+15aa"))',
    )
    datum_col: Optional[str] = Field(
        default=None,
        description="Datum kolom (optioneel), deze wordt onveranderd aan de output meegegeven",
    )
    opmerking_col: Optional[str] = Field(
        default=None,
        description="Opmerking kolom (optioneel), deze wordt onveranderd aan de output meegegeven",
    )
    output: Optional[Path] = Field(
        default=None,
        description="Output bestand (optioneel), indien niet gegeven wordt er een bestandsnaam gegenereerd",
    )


class Veg2HabConfig(BaseSettings):
    class Config:
        env_prefix = "VEG2HAB_"

    mozaiek_threshold: Union[int, float] = Field(
        default=95.0,  # todo number/float
        description="Threshold voor het bepalen of een vlak in het mozaiek ligt",
    )
    mozaiek_als_rand_langs_threshold: Union[int, float] = Field(
        default=50.0,  # todo number/float
        description="Threshold voor het bepalen of een vlak langs de rand van het mozaiek ligt",
    )
    niet_geautomatiseerde_sbb: List[str] = Field(
        default=[
            "100",
            "200",
            "300",
            "400",
        ],
        description="SBB vegetatietypen die niet geautomatiseerd kunnen worden",
    )


class Interface(metaclass=ABCMeta):
    """Singleton class that defines the interface for the different UI systems."""

    __instance = None

    # make the constructor private
    def __new__(cls):
        raise TypeError(
            "Interface is a singleton class and cannot only be accessed through get_instance"
        )

    @classmethod
    def get_instance(cls):
        if Interface.__instance is None:
            Interface.__instance = object.__new__(cls)
        return Interface.__instance

    def shape_id_to_filename(self, shapefile_id: str) -> Path:
        """Convert the shapefile id to a (temporary) file and returns the filename"""
        return Path(shapefile_id)

    @abstractmethod
    def output_shapefile(
        self, shapefile_id: Optional[Path], gdf: gpd.GeoDataFrame
    ) -> None:
        """Output the shapefile with the given id.
        ID would either be a path to a shapefile or an identifier to a shapefile in ArcGIS or QGIS.
        """

    @abstractmethod
    def instantiate_loggers(self, log_level: int) -> None:
        """Instantiate the loggers for the module."""

    def get_config(self) -> Veg2HabConfig:
        return Veg2HabConfig()
