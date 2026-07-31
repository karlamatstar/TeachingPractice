const getSizeMB = (size) => {
	return (size / 1024 / 1024).toFixed(2);
};

export { getSizeMB };
