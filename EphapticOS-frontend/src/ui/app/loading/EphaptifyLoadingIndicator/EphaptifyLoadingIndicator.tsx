import classNames from "classnames";
import styles from "./EphaptifyLoadingIndicator.module.css";

function EphaptifyLoadingIndicator({ isLoading = true }) {
  return (
    <div className={classNames(styles.donut1, isLoading && styles.spin)}>
      <div className={classNames(styles.donut2, isLoading && styles.spin)}>
        <div className={classNames(styles.donut3, isLoading && styles.spin)}>
          <div className={styles.dot} />
        </div>
      </div>
    </div>
  );
}

export default EphaptifyLoadingIndicator;
