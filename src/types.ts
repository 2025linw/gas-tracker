import type { Timestamp } from "firebase/firestore";

export type TTheme = "light" | "dark";
export type TThemeOptions = "system" | TTheme;

export type TRecord = {
  id: string;
  vehicleId: string;
  stationId: string;
  filledAt: Timestamp;
  gallons: number;
  pricePerGallon: number;
  totalCost: number;
  createdAt: Date;
  updatedAt: Date;
  deletedAt: Date;
};

export type TUser = {
  uid: string;
  themePref: "system" | "light" | "dark";
}

export type TVehicle = {
  uid: string,
  make: string,
  model?: string,
  year?: Date,

  color?: string,
}
