import styles from "./Button.module.css";

function Button({ children, onClick, type = "button", disabled, className = "" }) {
  return (
    <div className={className}>
      <button
        className={styles.button}
        type={type}
        onClick={onClick}
        disabled={disabled}
      >
        {children}
      </button>
    </div>
    );
}

export default Button
