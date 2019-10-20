Filevalidation = () => { 
	const imageFile = document.getElementById('image'); 
	// Check if any file is selected. 
	if (imageFile.files.length > 0) { 

		let imageLabel;
		let labels = document.getElementsByTagName('label');
		for( let x = 0; x < labels.length; x++ ) {
			if (labels[x].htmlFor == 'image') {
				imageLabel = labels[x];
			}
		}

		for (let i = 0; i <= imageFile.files.length - 1; i++) { 

			const fsize = imageFile.files.item(i).size; 
			const file = Math.round((fsize / 1024)); 

			if (file >= 1024) { 
				imageFile.value = '';
				imageLabel.innerHTML = 'Select Recipe Photo';
                
				alert( 
					'The image file is too big. Maximum allowed file size is 1Mb. Please select a smaller file size');		
			} else {
				imageLabel.innerHTML = imageFile.value;
				// document.getElementById('size').innerHTML = '<b>'
				// + imageFile + '</b> KB'; 
			} 
		} 
	} 
};


