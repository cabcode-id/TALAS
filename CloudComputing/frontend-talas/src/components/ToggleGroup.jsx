import { useState } from "react";
import styles from "./ToggleGroup.module.css"; // Mengimpor file CSS Module

function ToggleGroup() {
  const [colorationLevel, setColorationLevel] = useState("center");

  const handleChange = (event) => {
    setColorationLevel(event.target.value);
  };

  return (
<div className={styles.hiddenToggles}>
      {/* Left Button */}
      <input
        name="coloration-level"
        type="radio"
        id="coloration-left"
        value="left"
        className={styles.hiddenToggles__input}
        checked={colorationLevel === "left"}
        onChange={handleChange}
      />
      <label
        htmlFor="coloration-left"
        className={`${styles.hiddenToggles__label} ${
          colorationLevel === "left" ? styles.leftActive : ""
        }`}
      >
        Left
      </label>

      {/* Center Button */}
      <input
        name="coloration-level"
        type="radio"
        id="coloration-center"
        value="center"
        className={styles.hiddenToggles__input}
        checked={colorationLevel === "center"}
        onChange={handleChange}
      />
      <label
        htmlFor="coloration-center"
        className={`${styles.hiddenToggles__label} ${
          colorationLevel === "center" ? styles.centerActive : ""
        }`}
      >
        Center
      </label>

      {/* Right Button */}
      <input
        name="coloration-level"
        type="radio"
        id="coloration-right"
        value="right"
        className={styles.hiddenToggles__input}
        checked={colorationLevel === "right"}
        onChange={handleChange}
      />
      <label
        htmlFor="coloration-right"
        className={`${styles.hiddenToggles__label} ${
          colorationLevel === "right" ? styles.rightActive : ""
        }`}
      >
        Right
      </label>
    </div>
  );
}

export default ToggleGroup;
