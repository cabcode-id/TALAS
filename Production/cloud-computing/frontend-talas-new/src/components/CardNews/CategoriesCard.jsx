function CategoriesCard( {data} ) {
    return (
        <div className="hover:underline">
            <a href="#"> {data.name} </a>
        </div>
    );
}

export default CategoriesCard;