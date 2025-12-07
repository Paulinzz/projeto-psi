export function getIconByStatus(statusCode: number) {
    if (statusCode >= 200 && statusCode < 300 ) {
        return "success";
    } 
    else if (statusCode >= 400 && statusCode < 500) {
        return "error";
    }
    else if (statusCode >= 500){
        return "question" ;
    }
}